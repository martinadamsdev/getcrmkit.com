import { describe, it, expect, beforeEach } from "vitest";
import { useUIStore } from "./ui.store";

describe("useUIStore", () => {
  beforeEach(() => {
    useUIStore.setState({
      sidebarCollapsed: false,
      theme: "system",
      locale: "zh",
    });
  });

  it("has correct default state", () => {
    const state = useUIStore.getState();
    expect(state.sidebarCollapsed).toBe(false);
    expect(state.theme).toBe("system");
    expect(state.locale).toBe("zh");
  });

  it("toggles sidebar collapsed", () => {
    useUIStore.getState().toggleSidebar();
    expect(useUIStore.getState().sidebarCollapsed).toBe(true);

    useUIStore.getState().toggleSidebar();
    expect(useUIStore.getState().sidebarCollapsed).toBe(false);
  });

  it("sets theme", () => {
    useUIStore.getState().setTheme("dark");
    expect(useUIStore.getState().theme).toBe("dark");

    useUIStore.getState().setTheme("light");
    expect(useUIStore.getState().theme).toBe("light");
  });

  it("sets locale", () => {
    useUIStore.getState().setLocale("en");
    expect(useUIStore.getState().locale).toBe("en");

    useUIStore.getState().setLocale("zh");
    expect(useUIStore.getState().locale).toBe("zh");
  });
});
