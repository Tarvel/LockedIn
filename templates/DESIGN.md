---
name: LockedIn High-Contrast Brutalist
colors:
  surface: '#fff8f0'
  surface-dim: '#e2d9c7'
  surface-bright: '#fff8f0'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#fcf3e0'
  surface-container: '#f6eddb'
  surface-container-high: '#f0e7d5'
  surface-container-highest: '#ebe2cf'
  on-surface: '#1f1b10'
  on-surface-variant: '#4d4632'
  inverse-surface: '#353024'
  inverse-on-surface: '#f9f0dd'
  outline: '#7f765f'
  outline-variant: '#d1c6ab'
  surface-tint: '#725c00'
  primary: '#725c00'
  on-primary: '#ffffff'
  primary-container: '#ffd100'
  on-primary-container: '#6f5a00'
  inverse-primary: '#edc200'
  secondary: '#0041c9'
  on-secondary: '#ffffff'
  secondary-container: '#0356ff'
  on-secondary-container: '#e4e7ff'
  tertiary: '#bd0049'
  on-tertiary: '#ffffff'
  tertiary-container: '#ffc8cf'
  on-tertiary-container: '#b90048'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffe07f'
  primary-fixed-dim: '#edc200'
  on-primary-fixed: '#231b00'
  on-primary-fixed-variant: '#564500'
  secondary-fixed: '#dce1ff'
  secondary-fixed-dim: '#b6c4ff'
  on-secondary-fixed: '#001551'
  on-secondary-fixed-variant: '#0039b3'
  tertiary-fixed: '#ffd9dd'
  tertiary-fixed-dim: '#ffb2bd'
  on-tertiary-fixed: '#400013'
  on-tertiary-fixed-variant: '#900036'
  background: '#fff8f0'
  on-background: '#1f1b10'
  surface-variant: '#ebe2cf'
typography:
  display-xl:
    fontFamily: Inter
    fontSize: 80px
    fontWeight: '900'
    lineHeight: '1.0'
    letterSpacing: -0.04em
  headline-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '900'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '900'
    lineHeight: '1.2'
  body-lg:
    fontFamily: Space Grotesk
    fontSize: 20px
    fontWeight: '500'
    lineHeight: '1.5'
  body-md:
    fontFamily: Space Grotesk
    fontSize: 16px
    fontWeight: '500'
    lineHeight: '1.5'
  label-mono:
    fontFamily: Space Grotesk
    fontSize: 14px
    fontWeight: '700'
    lineHeight: '1.2'
spacing:
  unit: 4px
  xs: 8px
  sm: 16px
  md: 32px
  lg: 48px
  xl: 80px
  border-width: 4px
  shadow-offset: 8px
---

## Brand & Style

This design system is built on the principles of **Neo-Brutalism**, intentionally rejecting the soft, sanitized aesthetics of modern SaaS. It aims to evoke a sense of urgency, precision, and raw energy—perfect for an AI platform that "locks in" a user's focus and trajectory.

The visual language is aggressive yet playful, utilizing high-contrast outlines and vibrant accents to create a physical, tactile feel. It is designed for high-achievers, builders, and developers who value clarity over fluff and want a tool that feels as heavy and solid as the roadmaps it generates.

## Colors

The palette utilizes a "Solarized" cream base to maintain readability while the accent colors provide explosive visual interest.

- **Background:** Use `#FDF6E3` (Cream) for main surfaces to reduce eye strain compared to pure white.
- **Accents:** Use Yellow (`#FFD100`), Blue (`#0055FF`), Pink (`#FF0066`), and Green (`#33FF00`) as flat fills for buttons, cards, and progress indicators. 
- **Borders & Shadows:** Use absolute Black (`#000000`) for all structural lines and shadows. 

Avoid gradients or transparency. Every color must be flat and opaque to maintain the high-contrast "Gumroad" aesthetic.

## Typography

The typography strategy is built on extreme weight variance. 

- **Headlines:** Use **Inter Black** (900 weight). All headings must be **Uppercase**. Tracking should be tight to create a "blocky" wall of text effect.
- **Body & Technical Info:** Use **Space Grotesk**. Its geometric quirks complement the brutalist style while remaining highly legible for roadmap details and AI descriptions.
- **Micro-copy:** Use the monospaced stylistic sets of Space Grotesk for status labels and metadata to reinforce the technical, AI-driven nature of the platform.

## Layout & Spacing

This design system uses a strict 4px-based grid. 

- **Grid:** Use a 12-column fixed grid for desktop web views with 32px gutters. 
- **Padding:** Elements should have generous internal padding (minimum 24px) to balance the heavy 4px borders. 
- **Alignment:** Force horizontal and vertical alignment. Elements should look "locked" into their containers. Do not use centered layouts for body text; stick to left-aligned compositions to emphasize the raw, systematic structure.

## Elevation & Depth

Elevation is never represented by Z-axis blurring or lighting effects. Instead, depth is achieved through **Hard Offset Shadows**.

- **Shadow Style:** Solid black (`#000000`) at 100% opacity. 
- **Offset:** Shadows are typically offset 6px or 8px to the bottom-right (e.g., `box-shadow: 8px 8px 0px 0px #000000`).
- **Interaction:** On hover, buttons and interactive cards should "press down" by reducing the shadow offset to 2px or 0px, physically moving the element's position to simulate a mechanical click.

## Shapes

The shape language is strictly **Sharp**. 

- **Corners:** 0px border radius on all containers, buttons, and input fields. Roundness is forbidden as it softens the aggressive personality of the design system.
- **Borders:** Every container must have a minimum `4px` solid black border. 
- **Dividers:** Horizontal and vertical rules should also be `4px` black lines, effectively carving the interface into distinct, high-contrast zones.

## Components

### Buttons
Primary buttons use the flat Yellow (`#FFD100`) or Bright Blue (`#0055FF`) fill with 4px black borders. Text is Inter Black Uppercase. On hover, the button shifts +4px down and +4px right while the shadow disappears.

### Cards
Cards are the primary container for roadmap steps. Use the Cream background or a specific accent color for the header. All cards must have the 8px hard black shadow. 

### Input Fields
Inputs use a white background with a 4px black border. On focus, the border color remains black, but the background shifts to the Neon Green (`#33FF00`) or the shadow increases in size to indicate the field is "active."

### Chips/Tags
Small rectangular boxes with 2px borders (the only exception to the 4px rule) and no shadows. Use these for category tags like "AI-Generated," "Phase 1," or "High Priority."

### Roadmap Timeline
Vertical 4px black lines connecting sharp-edged nodes. Nodes should be 24px x 24px squares filled with accent colors, never circles.