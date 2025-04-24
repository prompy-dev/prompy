export function Footer() {
  return (
    <footer className="border-t bg-white/80 backdrop-blur-sm py-6">
      <div className="container mx-auto px-4 text-center text-sm text-gray-500">
        <p>© {new Date().getFullYear()} Prompy. All rights reserved.</p>
      </div>
    </footer>
  );
}