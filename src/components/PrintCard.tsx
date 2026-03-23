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
    <div className="group">
      <Link href={`/piece/${piece.id}`}>
        <div className="relative overflow-hidden mb-4">
          <Image
            src={piece.imageUrl}
            alt={`${piece.title} — ${piece.equation}`}
            width={800}
            height={550}
            className="w-full h-auto transition-opacity duration-700 group-hover:opacity-90"
            style={{ backgroundColor: piece.background }}
          />
        </div>
      </Link>
      <div className="space-y-1">
        <Link href={`/piece/${piece.id}`}>
          <h3 className="text-headline text-primary hover:opacity-70 transition-opacity duration-500">
            {piece.title}
          </h3>
        </Link>
        <EquationLabel equation={piece.equation} />
        {showBuyButton && (
          <div className="pt-3 flex items-center justify-between">
            <span className="text-body text-secondary">${piece.price}</span>
            <a
              href={piece.gumroadUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="px-4 py-2 border border-primary text-caption uppercase tracking-widest text-primary hover:bg-primary hover:text-bg transition-colors duration-500"
            >
              Download
            </a>
          </div>
        )}
      </div>
    </div>
  );
}
