'use client';

export function ConversationSkeleton() {
  return (
    <div className="space-y-4 animate-pulse">
      {/* Header skeleton */}
      <div className="h-10 bg-border rounded-lg w-1/3"></div>

      {/* Messages skeleton */}
      <div className="space-y-4">
        {[1, 2, 3].map((i) => (
          <div key={i} className={`flex gap-3 ${i % 2 === 0 ? 'justify-end' : ''}`}>
            {i % 2 === 0 ? null : (
              <div className="h-8 w-8 bg-border rounded-lg flex-shrink-0"></div>
            )}
            <div className={`flex-1 max-w-md space-y-2 ${i % 2 === 0 ? 'text-right' : ''}`}>
              <div className={`h-4 bg-border rounded ${i % 2 === 0 ? 'ml-auto w-2/3' : 'w-full'}`}></div>
              <div className={`h-4 bg-border rounded ${i % 2 === 0 ? 'ml-auto w-1/2' : 'w-3/4'}`}></div>
              <div className={`h-3 bg-border rounded w-20 ${i % 2 === 0 ? 'ml-auto' : ''}`}></div>
            </div>
            {i % 2 === 0 ? (
              <div className="h-8 w-8 bg-border rounded-lg flex-shrink-0"></div>
            ) : null}
          </div>
        ))}
      </div>
    </div>
  );
}
