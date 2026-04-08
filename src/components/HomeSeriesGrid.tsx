import Image from "next/image";
import Link from "next/link";
import type { Series } from "@/data/series";

interface HomeSeriesGridProps {
  series: Series;
  index: number;
}

export default function HomeSeriesGrid({ series, index }: HomeSeriesGridProps) {
  const isRight = index % 2 === 1;

  // Use homePieceIds if defined, otherwise first 5 pieces
  const homePieces = series.homePieceIds
    ? series.homePieceIds.map(id => series.pieces.find(p => p.id === id)!).filter(Boolean)
    : series.pieces.slice(0, 5);
  const heroPiece = homePieces[0];
  const supportingPieces = homePieces.slice(1);
  const twoUpLayout = homePieces.length === 2;
  const threeUpLayout = homePieces.length === 3;

  return (
    <div className="mb-32">
      <div className={`max-w-2xl ${isRight ? "md:ml-auto md:text-right" : "md:text-left"}`}>
        <h3 className="text-headline uppercase tracking-widest text-primary mb-1">
          {series.name}
        </h3>
        <p
          className={`text-body text-secondary italic ${
            series.homeDescriptor ? "mb-3" : "mb-6"
          }`}
        >
          {series.tagline}
        </p>
        {series.homeDescriptor && (
          <p className="text-caption md:text-[13px] text-muted mb-6">
            {series.homeDescriptor}
          </p>
        )}
      </div>

      {/* Desktop: two equal images when only 2 featured pieces */}
      {twoUpLayout ? (
        <div className="hidden md:grid grid-cols-2 gap-gallery-gap">
          {homePieces.map((piece) => (
            <Link
              key={piece.id}
              href={`/piece/${piece.id}`}
              className="relative block group"
            >
              <div
                className="relative overflow-hidden"
                style={{ backgroundColor: piece.background || series.background }}
              >
                <Image
                  src={piece.imageUrl}
                  alt={`${piece.title} — mathematical art print from the ${series.name} series by Geometry of Feeling`}
                  width={800}
                  height={550}
                  className="w-full h-auto block transition-transform duration-500 group-hover:scale-[1.03]"
                />
                <div className="absolute inset-0 bg-black/0 group-hover:bg-black/30 transition-colors duration-500 flex items-end justify-center pb-6">
                  <span className="text-caption uppercase tracking-widest text-white opacity-0 group-hover:opacity-100 transition-opacity duration-500">
                    {piece.title}
                  </span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      ) : threeUpLayout ? (
        /* Desktop: hero + two stacked supporting pieces */
        <div className="hidden md:grid grid-cols-3 gap-gallery-gap">
          {isRight ? (
            <>
              {/* Supporting pieces stacked on the left */}
              <div className="col-span-1 grid grid-rows-2 gap-gallery-gap">
                {supportingPieces.map((piece) => (
                  <Link
                    key={piece.id}
                    href={`/piece/${piece.id}`}
                    className="relative block group"
                  >
                    <div
                      className="relative overflow-hidden h-full"
                      style={{ backgroundColor: piece.background || series.background }}
                    >
                      <Image
                        src={piece.imageUrl}
                        alt={`${piece.title} — mathematical art print from the ${series.name} series by Geometry of Feeling`}
                        width={400}
                        height={275}
                        className="w-full h-full object-cover block transition-transform duration-500 group-hover:scale-[1.03]"
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
                  style={{ backgroundColor: heroPiece.background || series.background }}
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
                  style={{ backgroundColor: heroPiece.background || series.background }}
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
              {/* Supporting pieces stacked on the right */}
              <div className="col-span-1 grid grid-rows-2 gap-gallery-gap">
                {supportingPieces.map((piece) => (
                  <Link
                    key={piece.id}
                    href={`/piece/${piece.id}`}
                    className="relative block group"
                  >
                    <div
                      className="relative overflow-hidden h-full"
                      style={{ backgroundColor: piece.background || series.background }}
                    >
                      <Image
                        src={piece.imageUrl}
                        alt={`${piece.title} — mathematical art print from the ${series.name} series by Geometry of Feeling`}
                        width={400}
                        height={275}
                        className="w-full h-full object-cover block transition-transform duration-500 group-hover:scale-[1.03]"
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
      ) : (
      /* Desktop: hero + supporting grid */
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
                    style={{ backgroundColor: piece.background || series.background }}
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
                style={{ backgroundColor: heroPiece.background || series.background }}
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
                style={{ backgroundColor: heroPiece.background || series.background }}
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
                    style={{ backgroundColor: piece.background || series.background }}
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
      )}

      {/* Mobile: horizontal scroll carousel */}
      <div className="md:hidden relative">
        <div className="flex overflow-x-auto gap-4 scrollbar-hide -mx-6 px-6 snap-x snap-mandatory">
          {series.pieces.map((piece) => (
            <Link
              key={piece.id}
              href={`/piece/${piece.id}`}
              className="flex-shrink-0 block snap-start"
              style={{ width: "80vw" }}
            >
              <div
                className="overflow-hidden"
                style={{ backgroundColor: piece.background || series.background }}
              >
                <Image
                  src={piece.imageUrl}
                  alt={`${piece.title} — mathematical art print from the ${series.name} series by Geometry of Feeling`}
                  width={600}
                  height={413}
                  className="w-full h-auto block"
                />
              </div>
              <div className="flex items-baseline justify-between mt-2 px-1">
                <p className="text-caption text-secondary truncate">
                  {piece.title}
                </p>
                <p className="text-caption text-muted flex-shrink-0 ml-2">
                  From ${piece.price}
                </p>
              </div>
            </Link>
          ))}
        </div>
        {/* Right-edge gradient to signal scrollability */}
        <div className="absolute right-0 top-0 bottom-8 w-12 bg-gradient-to-l from-bg to-transparent pointer-events-none" />
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
