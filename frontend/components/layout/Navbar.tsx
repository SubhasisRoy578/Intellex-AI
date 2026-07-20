'use client';

import { LogOut, Settings, User, Menu, X } from 'lucide-react';
import Link from 'next/link';
import { useState } from 'react';

interface NavbarProps {
  onMenuToggle?: () => void;
  isMenuOpen?: boolean;
}

export function Navbar({ onMenuToggle, isMenuOpen }: NavbarProps) {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  return (
    <nav className="sticky top-0 z-40 w-full border-b border-border bg-card/80 backdrop-blur-lg">
      <div className="flex h-16 items-center justify-between px-4 md:px-6">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-gold to-amber">
            <span className="text-lg font-bold text-background">I</span>
          </div>
          <span className="hidden font-bold text-text-primary sm:inline">Intellex</span>
        </Link>

        {/* Center - Navigation Links (hidden on mobile) */}
        <div className="hidden gap-6 md:flex">
          <Link href="/dashboard" className="text-sm text-text-secondary hover:text-gold transition-colors">
            Dashboard
          </Link>
          <Link href="/#features" className="text-sm text-text-secondary hover:text-gold transition-colors">
            Features
          </Link>
          <Link href="/#pricing" className="text-sm text-text-secondary hover:text-gold transition-colors">
            Pricing
          </Link>
        </div>

        {/* Right - User Menu */}
        <div className="flex items-center gap-4">
          {/* Desktop Menu Button */}
          <button
            onClick={() => setIsDropdownOpen(!isDropdownOpen)}
            className="hidden md:flex items-center gap-2 rounded-lg bg-surface border border-border px-4 py-2 text-sm text-text-primary hover:border-gold/50 transition-colors"
          >
            <User className="h-4 w-4" />
            <span>Account</span>
          </button>

          {/* Mobile Menu Toggle */}
          <button
            onClick={onMenuToggle}
            className="md:hidden text-text-secondary hover:text-gold transition-colors"
            aria-label="Toggle menu"
          >
            {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>

          {/* Dropdown Menu */}
          {isDropdownOpen && (
            <div className="absolute right-4 top-16 mt-2 w-48 rounded-lg border border-border bg-card shadow-lg">
              <Link
                href="/dashboard/profile"
                className="flex items-center gap-2 px-4 py-3 text-sm text-text-secondary hover:bg-hover hover:text-gold transition-colors border-b border-border"
              >
                <User className="h-4 w-4" />
                Profile
              </Link>
              <Link
                href="/dashboard/settings"
                className="flex items-center gap-2 px-4 py-3 text-sm text-text-secondary hover:bg-hover hover:text-gold transition-colors border-b border-border"
              >
                <Settings className="h-4 w-4" />
                Settings
              </Link>
              <button className="w-full flex items-center gap-2 px-4 py-3 text-sm text-error hover:bg-hover transition-colors">
                <LogOut className="h-4 w-4" />
                Sign Out
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
