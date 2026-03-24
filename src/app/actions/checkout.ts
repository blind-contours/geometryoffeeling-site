"use server";

import { getStripe } from "@/lib/stripe";
import { getSizeById, SHIPPING_COUNTRIES } from "@/lib/products";
import { getPieceBySlug } from "@/data/series";
import type Stripe from "stripe";

export async function createCheckoutSession(pieceId: string, sizeId: string) {
  const piece = getPieceBySlug(pieceId);
  if (!piece) throw new Error("Piece not found");

  const size = getSizeById(sizeId);
  if (!size) throw new Error("Invalid size");

  const baseUrl = process.env.NEXT_PUBLIC_URL || "http://localhost:3000";

  const session = await getStripe().checkout.sessions.create({
    mode: "payment",
    line_items: [
      {
        price_data: {
          currency: "usd",
          unit_amount: size.priceCents,
          product_data: {
            name: `${piece.title} — ${size.label}`,
            description: `Fine art print on Hahnemuhle German Etching 310gsm`,
            images: [`${baseUrl}${piece.imageUrl}`],
          },
        },
        quantity: 1,
      },
    ],
    shipping_address_collection: {
      allowed_countries:
        SHIPPING_COUNTRIES as Stripe.Checkout.SessionCreateParams.ShippingAddressCollection.AllowedCountry[],
    },
    shipping_options: [
      {
        shipping_rate_data: {
          type: "fixed_amount",
          fixed_amount: { amount: 0, currency: "usd" },
          display_name: "Standard Shipping",
          delivery_estimate: {
            minimum: { unit: "business_day", value: 5 },
            maximum: { unit: "business_day", value: 10 },
          },
        },
      },
    ],
    metadata: {
      pieceId: piece.id,
      sizeId: size.id,
      prodigiSku: size.prodigiSku,
    },
    success_url: `${baseUrl}/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${baseUrl}/piece/${piece.id}`,
  });

  if (!session.url) throw new Error("Failed to create checkout session");
  return session.url;
}
