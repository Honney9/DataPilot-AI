export function CardSkeleton({ height = "h-32" }: { height?: string }) {
  return <div className={`rounded-xl border border-border bg-card animate-pulse ${height}`} />;
}
export function GridSkeleton({ count = 4, height = "h-32" }: { count?: number; height?: string }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {Array.from({ length: count }).map((_, i) => <CardSkeleton key={i} height={height} />)}
    </div>
  );
}