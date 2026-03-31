import Image from "next/image";
import Link from "next/link";
import EquationLabel from "./EquationLabel";
import type { Piece } from "@/data/series";

interface PrintCardProps {
  piece: Piece;
  showBuyButton?: boolean;
}

export default function PrintCard({
  piece,
  showBuyButton = false,
}: PrintCardProps) {
  return (
    <div className="group transition-shadow duration-500 hover:shadow-[0_8px_30px_rgba(0,0,0,0.08)]">
      <Link href={`/piece/${piece.id}`}>
        <div className="relative overflow-hidden mb-4">
          <Image
            src={piece.imageUrl}
            alt={`${piece.title} — minimalist mathematical fine art print from the ${piece.series} series by Geometry of Feeling`}
            width={800}
            height={550}
            className="w-full h-auto transition-transform duration-700 group-hover:scale-[1.03]"
            style={{ backgroundColor: piece.background }}
          />
        </div>
      </Link>
      <div className="space-y-1">
        <Link href={`/piece/${piece.id}`}>
          <h3 className="text-headline text-primary hover:text-secondary transition-colors duration-500">
            {piece.title}
          </h3>
        </Link>
        <EquationLabel equation={piece.equation} />
        {showBuyButton && (
          <div className="pt-3 flex items-center justify-between">
            <span className="text-caption text-secondary">From ${piece.price}</span>
            <Link
              href={`/piece/${piece.id}`}
              className="px-4 py-2 bg-primary text-bg text-caption uppercase tracking-widest hover:opacity-90 transition-opacity duration-500"
            >
              View
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}
