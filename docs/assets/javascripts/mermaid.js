document$.subscribe(() => {
  mermaid.initialize({
    startOnLoad: false,
    securityLevel: "loose",
    theme: document.body.getAttribute("data-md-color-scheme") === "slate" ? "dark" : "neutral",
    themeVariables: {
      primaryColor: "#6750e6",
      primaryTextColor: "#ffffff",
      lineColor: "#667085",
      fontFamily: "var(--md-text-font-family)",
    },
  });
  mermaid.run({ nodes: document.querySelectorAll(".mermaid") });
});

