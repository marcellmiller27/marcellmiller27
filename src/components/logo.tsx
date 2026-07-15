type LogoProps = {
  size?: number;
  title?: string;
};

/**
 * John Henry Investments emblem: the "Jh" monogram in brand gold on a trust-navy
 * badge (matching the firm mark). Inline SVG so it stays crisp at any size and
 * inherits the brand palette. (A tech-forward mark is planned to follow.)
 */
export function Logo({ size = 40, title = "John Henry Investments" }: LogoProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 48 48"
      role="img"
      aria-label={title}
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <linearGradient id="jhNavy" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#0c2438" />
          <stop offset="1" stopColor="#06121f" />
        </linearGradient>
        <linearGradient id="jhGold" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#f2d68c" />
          <stop offset="1" stopColor="#c1913f" />
        </linearGradient>
      </defs>
      <rect
        x="3"
        y="3"
        width="42"
        height="42"
        rx="12"
        fill="url(#jhNavy)"
        stroke="#e3b765"
        strokeWidth="1.5"
        strokeOpacity="0.85"
      />
      <text
        x="24"
        y="25"
        textAnchor="middle"
        dominantBaseline="central"
        fontFamily="Georgia, 'Times New Roman', serif"
        fontSize="25"
        fontWeight="500"
        letterSpacing="0.5"
        fill="url(#jhGold)"
      >
        Jh
      </text>
    </svg>
  );
}
