import { createElement, forwardRef, type ReactNode } from "react";

const motionOnlyProps = new Set([
  "animate",
  "custom",
  "exit",
  "initial",
  "layout",
  "layoutId",
  "transition",
  "variants",
  "viewport",
  "whileFocus",
  "whileHover",
  "whileInView",
  "whileTap",
]);

function staticElement(tag: string) {
  return forwardRef<HTMLElement, Record<string, unknown>>(function StaticElement(props, ref) {
    const clean: Record<string, unknown> = {};
    const finalState =
      typeof props["animate"] === "object" && props["animate"] !== null
        ? (props["animate"] as Record<string, unknown>)
        : typeof props["whileInView"] === "object" && props["whileInView"] !== null
          ? (props["whileInView"] as Record<string, unknown>)
          : {};
    const style = { ...((props["style"] as Record<string, unknown> | undefined) ?? {}) };

    for (const [key, value] of Object.entries(props)) {
      if (!motionOnlyProps.has(key)) clean[key] = value;
    }

    for (const [key, value] of Object.entries(finalState)) {
      if (["backgroundColor", "color", "height", "opacity", "width"].includes(key)) {
        style[key] = value;
      } else if (["fill", "pathLength", "strokeDashoffset"].includes(key)) {
        clean[key] = value;
      }
    }

    if (Object.keys(style).length > 0) clean["style"] = style;
    return createElement(tag, { ...clean, ref });
  });
}

export const motion = {
  circle: staticElement("circle"),
  div: staticElement("div"),
  line: staticElement("line"),
  path: staticElement("path"),
  span: staticElement("span"),
};

export function AnimatePresence({ children }: { children: ReactNode; mode?: string }) {
  return children;
}
