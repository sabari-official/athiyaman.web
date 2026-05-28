/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#0B3C5D",
        secondary: "#328CC1",
        "primary-soft": "#F0F4FF",
        "deep-blue": "#082b43",
        background: "#F8FAFC",
        surface: "#FFFFFF",
        text: "#1E293B",
        success: "#10B981",
        "success-foreground": "#FFFFFF",
        "success-soft": "#D1FAE5",
        warning: "#F59E0B",
        "warning-foreground": "#78350F",
        "warning-soft": "#FEF3C7",
        danger: "#EF4444",
        "danger-soft": "#FEE2E2",
        muted: "#F1F5F9",
        "muted-foreground": "#64748B",
        border: "#E2E8F0",
      },
      fontFamily: {
        sans: ["'Plus Jakarta Sans'", 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        card: "0 1px 3px rgba(15, 23, 42, 0.08), 0 1px 2px rgba(15, 23, 42, 0.05)",
        modal: "0 20px 60px rgba(15, 23, 42, 0.18)",
        btn: "0 1px 2px rgba(11, 60, 93, 0.25)",
      },
      backgroundImage: {
        "nav-gradient": "linear-gradient(90deg, #0B3C5D 0%, #328CC1 100%)",
      }
    },
  },
  plugins: [],
}
