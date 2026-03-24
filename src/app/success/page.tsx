import Link from "next/link";
import { getStripe } from "@/lib/stripe";
import type { Metadata } from "next";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Order Confirmed — Geometry of Feeling",
};

interface Props {
  searchParams: { session_id?: string };
}

export default async function SuccessPage({ searchParams }: Props) {
  let pieceTitle: string | null = null;
  let sizeLabel: string | null = null;

  if (searchParams.session_id) {
    try {
      const s = getStripe();
      const session = await s.checkout.sessions.retrieve(
        searchParams.session_id
      );
      // Get info from line items
      const lineItems = await s.checkout.sessions.listLineItems(
        session.id,
        { limit: 1 }
      );
      if (lineItems.data.length > 0) {
        pieceTitle = lineItems.data[0].description;
      }
      if (session.metadata) {
        const { getSizeById } = await import("@/lib/products");
        const size = getSizeById(session.metadata.sizeId);
        sizeLabel = size?.label || null;
      }
    } catch {
      // Session retrieval failed — show generic success
    }
  }

  return (
    <div className="pt-20 pb-24">
      <div className="max-w-content mx-auto px-6">
        <div className="max-w-xl mx-auto text-center">
          <h1 className="text-2xl font-mono font-light text-primary mb-4">
            Thank you for your order
          </h1>

          {pieceTitle && (
            <p className="text-body text-primary mb-2">{pieceTitle}</p>
          )}
          {sizeLabel && (
            <p className="text-caption text-secondary mb-6">{sizeLabel}</p>
          )}

          <div className="border border-border p-6 mb-8 text-left">
            <p className="text-body text-secondary mb-3">
              Your print is being prepared on Hahnemuhle German Etching paper
              and will ship within 5–10 business days.
            </p>
            <p className="text-caption text-muted">
              You&apos;ll receive a shipping confirmation email with tracking
              once your order is on its way.
            </p>
          </div>

          <Link
            href="/series"
            className="inline-block px-6 py-3 border border-primary text-primary text-caption uppercase tracking-widest hover:bg-primary hover:text-bg transition-all duration-500"
          >
            Browse more prints
          </Link>
        </div>
      </div>
    </div>
  );
}
