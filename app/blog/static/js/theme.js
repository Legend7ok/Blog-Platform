(() => {
  const storageKey = "theme";
  const root = document.documentElement;
  const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
  const ACTIVE_CLASSES =
    "rounded-full bg-purple-100 px-2.5 py-0.5 text-sm whitespace-nowrap text-purple-700 dark:bg-purple-700 dark:text-purple-100";
  const INACTIVE_CLASSES =
    "rounded-full border border-purple-500 px-2.5 py-0.5 text-sm whitespace-nowrap text-purple-700 dark:text-purple-100";

  const getButtons = () =>
    Array.from(document.querySelectorAll("[data-theme-toggle]"));

  const getStoredTheme = () => {
    try {
      return localStorage.getItem(storageKey);
    } catch (err) {
      return null;
    }
  };

  const getSystemTheme = () => (mediaQuery.matches ? "dark" : "light");

  const updateToggleUI = (theme) => {
    const buttons = getButtons();
    buttons.forEach((button) => {
      const light = button.querySelector('[data-theme-option="light"]');
      const dark = button.querySelector('[data-theme-option="dark"]');

      if (light && dark) {
        if (theme === "dark") {
          dark.className = ACTIVE_CLASSES;
          light.className = INACTIVE_CLASSES;
        } else {
          light.className = ACTIVE_CLASSES;
          dark.className = INACTIVE_CLASSES;
        }
      }

      button.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
    });
  };

  const applyTheme = (theme, persist = false) => {
    const normalized = theme === "dark" ? "dark" : "light";

    if (normalized === "dark") {
      root.classList.add("dark");
    } else {
      root.classList.remove("dark");
    }

    root.setAttribute("data-theme", normalized);
    updateToggleUI(normalized);

    if (persist) {
      try {
        localStorage.setItem(storageKey, normalized);
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
    const current =
      root.getAttribute("data-theme") ||
      (root.classList.contains("dark") ? "dark" : "light");
    const nextTheme = current === "dark" ? "light" : "dark";
    applyTheme(nextTheme, true);
  };

  initTheme();

  if (mediaQuery.addEventListener) {
    mediaQuery.addEventListener("change", handleSystemChange);
  } else if (mediaQuery.addListener) {
    mediaQuery.addListener(handleSystemChange);
  }

  getButtons().forEach((button) => {
    button.addEventListener("click", handleToggle);
  });
})();
