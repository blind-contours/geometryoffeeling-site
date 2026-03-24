import { NextRequest, NextResponse } from "next/server";
import { getStripe } from "@/lib/stripe";
import { createOrder } from "@/lib/prodigi";
import { sendOrderConfirmation } from "@/lib/email";
import { list } from "@vercel/blob";
import type Stripe from "stripe";

const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET!;

async function getHighResUrl(pieceId: string): Promise<string | null> {
  try {
    const { blobs } = await list({ prefix: `prints/${pieceId}`, limit: 1 });
    if (blobs.length > 0) return blobs[0].downloadUrl;
  } catch (err) {
    console.error("Failed to find blob for piece:", pieceId, err);
  }
  return null;
}

export async function POST(req: NextRequest) {
  const body = await req.text();
  const signature = req.headers.get("stripe-signature");

  if (!signature) {
    return NextResponse.json({ error: "No signature" }, { status: 400 });
  }

  let event: Stripe.Event;
  try {
    event = getStripe().webhooks.constructEvent(body, signature, webhookSecret);
  } catch (err) {
    console.error("Webhook signature verification failed:", err);
    return NextResponse.json({ error: "Invalid signature" }, { status: 400 });
  }

  if (event.type === "checkout.session.completed") {
    const session = event.data.object as Stripe.Checkout.Session;

    // Retrieve full session with collected information
    const fullSession = await getStripe().checkout.sessions.retrieve(session.id, {
      expand: ["collected_information"],
    });

    const { pieceId, sizeId, prodigiSku } = fullSession.metadata || {};
    if (!pieceId || !sizeId || !prodigiSku) {
      console.error("Missing metadata on session:", fullSession.id);
      return NextResponse.json({ error: "Missing metadata" }, { status: 400 });
    }

    const shipping =
      fullSession.collected_information?.shipping_details;
    if (!shipping?.address) {
      console.error("No shipping address on session:", fullSession.id);
      return NextResponse.json(
        { error: "No shipping address" },
        { status: 400 }
      );
    }

    // Get high-res file URL from Vercel Blob, fall back to public image
    let imageUrl = await getHighResUrl(pieceId);
    if (!imageUrl) {
      const baseUrl =
        process.env.NEXT_PUBLIC_URL || "https://geometryoffeeling.com";
      const { getPieceBySlug } = await import("@/data/series");
      const piece = getPieceBySlug(pieceId);
      imageUrl = piece
        ? `${baseUrl}${piece.imageUrl}`
        : `${baseUrl}/prints/${pieceId}.jpg`;
      console.warn(
        `Using fallback image URL for ${pieceId} — upload high-res to Vercel Blob`
      );
    }

    const addr = shipping.address;
    try {
      await createOrder(
        {
          name: shipping.name || "Customer",
          address: {
            line1: addr.line1 || "",
            line2: addr.line2 || undefined,
            postalOrZipCode: addr.postal_code || "",
            countryCode: addr.country || "US",
            townOrCity: addr.city || "",
            stateOrCounty: addr.state || undefined,
          },
        },
        prodigiSku,
        imageUrl,
        `${pieceId}-${sizeId}-${fullSession.id}`,
        fullSession.id // idempotency key
      );
      console.log("Prodigi order created for session:", fullSession.id);
    } catch (err) {
      console.error("Failed to create Prodigi order:", err);
      // Don't return 500 — Stripe would retry and we'd double-process
      // Log for manual fulfillment
    }

    // Send order confirmation email
    const customerEmail = fullSession.customer_details?.email;
    if (customerEmail) {
      try {
        const { getPieceBySlug } = await import("@/data/series");
        const { getSizeById } = await import("@/lib/products");
        const piece = getPieceBySlug(pieceId);
        const size = getSizeById(sizeId);
        const baseUrl = process.env.NEXT_PUBLIC_URL || "https://geometryoffeeling.com";

        await sendOrderConfirmation({
          to: customerEmail,
          customerName: shipping.name?.split(" ")[0] || "",
          pieceTitle: piece?.title || pieceId,
          sizeLabel: size?.label || sizeId,
          imageUrl: piece ? `${baseUrl}${piece.imageUrl}` : imageUrl,
          equation: piece?.equation || "",
        });
        console.log("Confirmation email sent to:", customerEmail);
      } catch (err) {
        console.error("Failed to send confirmation email:", err);
        // Non-fatal — order still fulfilled
      }
    }
  }

  return NextResponse.json({ received: true });
}
