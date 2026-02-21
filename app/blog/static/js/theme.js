(() => {
  const storageKey = "theme";
  const root = document.documentElement;
  const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
  const buttons = Array.from(document.querySelectorAll("[data-theme-toggle]"));

  const getStoredTheme = () => {
    try {
      return localStorage.getItem(storageKey);
    } catch (err) {
      return null;
    }
  };

  const getSystemTheme = () => (mediaQuery.matches ? "dark" : "light");

  const applyTheme = (theme, persist = false) => {
    if (theme === "dark") {
      root.classList.add("dark");
    } else {
      root.classList.remove("dark");
    }

    buttons.forEach((button) => {
      button.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
    });

    if (persist) {
      try {
        localStorage.setItem(storageKey, theme);
      } catch (err) {
        // Ignore storage errors
      }
    }
  };

  const initTheme = () => {
    const stored = getStoredTheme();
    if (stored === "dark" || stored === "light") {
      applyTheme(stored, false);
    } else {
      applyTheme(getSystemTheme(), false);
    }
  };

  const handleSystemChange = () => {
    const stored = getStoredTheme();
    if (stored === "dark" || stored === "light") {
      return;
    }
    applyTheme(getSystemTheme(), false);
  };

  const handleToggle = () => {
    const isDark = root.classList.contains("dark");
    const nextTheme = isDark ? "light" : "dark";
    applyTheme(nextTheme, true);
  };

  initTheme();

  if (mediaQuery.addEventListener) {
    mediaQuery.addEventListener("change", handleSystemChange);
  } else if (mediaQuery.addListener) {
    mediaQuery.addListener(handleSystemChange);
  }

  buttons.forEach((button) => {
    button.addEventListener("click", handleToggle);
  });
})();
