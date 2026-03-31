import Image from "next/image";
import Link from "next/link";
import type { Series } from "@/data/series";

interface HomeSeriesGridProps {
  series: Series;
  index: number;
}

export default function HomeSeriesGrid({ series, index }: HomeSeriesGridProps) {
  const isRight = index % 2 === 1;
  const pieces = series.pieces.slice(0, 5);
  const heroPiece = pieces[0];
  const supportingPieces = pieces.slice(1);

  return (
    <div className="mb-32">
      <div className={`max-w-2xl ${isRight ? "md:ml-auto md:text-right" : "md:text-left"}`}>
        <h3 className="text-headline uppercase tracking-widest text-primary mb-1">
          {series.name}
        </h3>
        <p className="text-body text-secondary italic mb-6">{series.tagline}</p>
      </div>

      {/* Desktop: hero + supporting grid */}
      <div className="hidden md:grid grid-cols-4 gap-gallery-gap">
        {/* Hero piece — 2 cols, 2 rows */}
        {isRight ? (
          <>
            {/* Supporting pieces on the left */}
            <div className="col-span-2 grid grid-cols-2 gap-gallery-gap">
              {supportingPieces.map((piece) => (
                <Link
                  key={piece.id}
                  href={`/piece/${piece.id}`}
                  className="relative block group"
                >
                  <div
                    className="relative overflow-hidden"
                    style={{ backgroundColor: series.background }}
                  >
                    <Image
                      src={piece.imageUrl}
                      alt={`${piece.title} — mathematical art print from the ${series.name} series by Geometry of Feeling`}
                      width={400}
                      height={275}
                      className="w-full h-auto block transition-transform duration-500 group-hover:scale-[1.03]"
                    />
                    <div className="absolute inset-0 bg-black/0 group-hover:bg-black/30 transition-colors duration-500 flex items-end justify-center pb-4">
                      <span className="text-caption uppercase tracking-widest text-white opacity-0 group-hover:opacity-100 transition-opacity duration-500">
                        {piece.title}
                      </span>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
            {/* Hero on the right */}
            <Link
              href={`/piece/${heroPiece.id}`}
              className="col-span-2 relative block group"
            >
              <div
                className="relative overflow-hidden h-full"
                style={{ backgroundColor: series.background }}
              >
                <Image
                  src={heroPiece.imageUrl}
                  alt={`${heroPiece.title} — mathematical art print from the ${series.name} series by Geometry of Feeling`}
                  width={800}
                  height={550}
                  className="w-full h-full object-cover block transition-transform duration-500 group-hover:scale-[1.03]"
                />
                <div className="absolute inset-0 bg-black/0 group-hover:bg-black/30 transition-colors duration-500 flex items-end justify-center pb-6">
                  <span className="text-caption uppercase tracking-widest text-white opacity-0 group-hover:opacity-100 transition-opacity duration-500">
                    {heroPiece.title}
                  </span>
                </div>
              </div>
            </Link>
          </>
        ) : (
          <>
            {/* Hero on the left */}
            <Link
              href={`/piece/${heroPiece.id}`}
              className="col-span-2 relative block group"
            >
              <div
                className="relative overflow-hidden h-full"
                style={{ backgroundColor: series.background }}
              >
                <Image
                  src={heroPiece.imageUrl}
                  alt={`${heroPiece.title} — mathematical art print from the ${series.name} series by Geometry of Feeling`}
                  width={800}
                  height={550}
                  className="w-full h-full object-cover block transition-transform duration-500 group-hover:scale-[1.03]"
                />
                <div className="absolute inset-0 bg-black/0 group-hover:bg-black/30 transition-colors duration-500 flex items-end justify-center pb-6">
                  <span className="text-caption uppercase tracking-widest text-white opacity-0 group-hover:opacity-100 transition-opacity duration-500">
                    {heroPiece.title}
                  </span>
                </div>
              </div>
            </Link>
            {/* Supporting pieces on the right */}
            <div className="col-span-2 grid grid-cols-2 gap-gallery-gap">
              {supportingPieces.map((piece) => (
                <Link
                  key={piece.id}
                  href={`/piece/${piece.id}`}
                  className="relative block group"
                >
                  <div
                    className="relative overflow-hidden"
                    style={{ backgroundColor: series.background }}
                  >
                    <Image
                      src={piece.imageUrl}
                      alt={`${piece.title} — mathematical art print from the ${series.name} series by Geometry of Feeling`}
                      width={400}
                      height={275}
                      className="w-full h-auto block transition-transform duration-500 group-hover:scale-[1.03]"
                    />
                    <div className="absolute inset-0 bg-black/0 group-hover:bg-black/30 transition-colors duration-500 flex items-end justify-center pb-4">
                      <span className="text-caption uppercase tracking-widest text-white opacity-0 group-hover:opacity-100 transition-opacity duration-500">
                        {piece.title}
                      </span>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </>
        )}
      </div>

      {/* Mobile: horizontal scroll row (unchanged) */}
      <div className="md:hidden relative">
        <div className="flex overflow-x-auto gap-3 scrollbar-hide -mx-6 px-6 snap-x snap-mandatory">
          {series.pieces.map((piece) => (
            <Link
              key={piece.id}
              href={`/piece/${piece.id}`}
              className="flex-shrink-0 block snap-start"
              style={{ width: "65vw" }}
            >
              <div
                className="overflow-hidden"
                style={{ backgroundColor: series.background }}
              >
                <Image
                  src={piece.imageUrl}
                  alt={`${piece.title} — mathematical art print from the ${series.name} series by Geometry of Feeling`}
                  width={240}
                  height={165}
                  className="w-full h-auto block"
                />
              </div>
              <p className="text-center text-caption text-secondary mt-1 truncate px-1">
                {piece.title}
              </p>
            </Link>
          ))}
        </div>
        {/* Right-edge gradient to signal scrollability */}
        <div className="absolute right-0 top-0 bottom-6 w-8 bg-gradient-to-l from-bg to-transparent pointer-events-none" />
      </div>

      <div className={`mt-10 ${isRight ? "md:text-right" : ""}`}>
        <Link
          href={`/series/${series.id}`}
          className="inline-block text-caption md:text-[13px] uppercase tracking-widest text-primary border-b border-primary/30 pb-1 hover:border-primary transition-colors duration-500"
        >
          Explore series &rarr;
        </Link>
      </div>
    </div>
  );
}
