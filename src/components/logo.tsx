// JHI-SIG: 69M2705M | Frontend shell | John Henry Investments (proprietary)
type LogoProps = {
  size?: number;
  title?: string;
};

/**
 * John Henry Investments emblem: a trust-navy badge with ascending growth bars
 * shaded emerald (growth) into gold (premium), topped by a gold upward arrow.
 * Drawn as inline SVG so it stays crisp and inherits the brand palette.
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
        <linearGradient id="jhGrowth" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#e9c877" />
          <stop offset="1" stopColor="#1fc585" />
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
      <g fill="url(#jhGrowth)">
        <rect x="11" y="29" width="5" height="8" rx="1.5" />
        <rect x="18" y="24" width="5" height="13" rx="1.5" />
        <rect x="25" y="19" width="5" height="18" rx="1.5" />
        <rect x="32" y="15" width="5" height="22" rx="1.5" />
      </g>
      <path d="M34.5 7 L39 13.5 L30 13.5 Z" fill="#e3b765" />
    </svg>
  );
}
