import Image from "next/image";
import Link from "next/link";
import type { Series } from "@/data/series";

interface SeriesCardProps {
  series: Series;
}

export default function SeriesCard({ series }: SeriesCardProps) {
  return (
    <div className="group">
      <Link href={`/series/${series.id}`}>
        <div className="mb-6">
          <h3 className="text-headline uppercase tracking-widest text-primary mb-1">
            {series.name}
          </h3>
          <p className="text-body text-secondary italic">{series.tagline}</p>
        </div>

        {/* 2-image preview */}
        <div className="grid grid-cols-2 gap-1 mb-4">
          {series.pieces.slice(0, 2).map((piece) => (
            <div
              key={piece.id}
              className="relative overflow-hidden"
              style={{ backgroundColor: series.background }}
            >
              <Image
                src={piece.imageUrl}
                alt={piece.title}
                width={400}
                height={275}
                className="w-full h-auto transition-opacity duration-700 group-hover:opacity-90"
              />
            </div>
          ))}
        </div>

        <p className="text-caption uppercase tracking-widest text-secondary group-hover:text-primary transition-colors duration-500">
          Explore series &rarr;
        </p>
      </Link>
    </div>
  );
}
