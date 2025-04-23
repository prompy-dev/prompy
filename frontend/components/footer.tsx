export function Footer() {
  return (
    <footer className="w-full border-t py-4 bg-background">
      <div className="container flex flex-col items-center justify-center gap-2 md:flex-row md:justify-between text-sm">
        <p className="text-center text-sm text-muted-foreground md:text-left">
          &copy; {new Date().getFullYear()} Prompy. All rights reserved.
        </p>
        <p className="text-center text-sm text-muted-foreground md:text-right">
          Crafted with ❤️ for prompt engineers
        </p>
      </div>
    </footer>
  );
}