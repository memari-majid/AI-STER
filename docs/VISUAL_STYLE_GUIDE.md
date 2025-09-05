# AI-STER Visual Style Guide

## Overview
This guide documents the visual design principles for the AI-STER application, following Utah Valley University's official brand guidelines.

## Core Principles

### 1. Rule of Ratio
Following UVU's brand guidelines, we implement a hierarchy of color usage:
- **Primary colors (80%)**: UVU Green (#185C33) and White (#FFFFFF)
- **Secondary colors (15%)**: Used sparingly for support
- **Accent colors (5%)**: Minimal use for highlights only

### 2. Clean & Professional
- Emphasize white space and breathing room
- Minimal use of shadows and effects
- No excessive animations or transitions
- Professional, academic appearance

## Color Palette

### Primary Colors
- **UVU Green**: `#185C33` - Main brand color, used for headers, buttons, and key elements
- **White**: `#FFFFFF` - Primary background, ensures clarity and space

### Secondary Colors
- **Wolverine Green**: `#008A40` - Sparingly used for hover states
- **Grey**: `#AAAAAB` - Text labels, subtle borders
- **Warm**: `#F2F0EB` - Light background for sidebar and subtle sections
- **Black**: `#000000` - Body text

### Accent Colors (Use Minimally)
- **Valley Rise**: `#78BE3F` - Success states only
- **Lake Calm**: `#87C7BA` - Info messages only
- **Heritage Brick**: `#B45336` - Error states only
- **Legacy Gold**: `#D2AC5F` - Warning states only

## Typography

### Font Families
- **Headers**: Rajdhani (weight: 600)
- **Body Text**: Inter (weights: 400, 500, 600)

### Font Sizes
- **H1**: 2.5rem
- **H2**: 1.8rem
- **H3**: 1.4rem
- **Body**: 1rem
- **Small**: 0.875rem

## Component Styling

### Headers
```css
color: #185C33;
font-family: 'Rajdhani', sans-serif;
font-weight: 600;
/* No underlines or excessive decoration */
```

### Buttons
**Primary Button**
```css
background-color: #185C33;
color: #FFFFFF;
border: none;
border-radius: 6px;
padding: 0.5rem 1.5rem;
```

**Secondary Button**
```css
background-color: #FFFFFF;
color: #185C33;
border: 2px solid #185C33;
border-radius: 6px;
```

### Forms
- Light grey borders (#d0d0d0)
- Green focus state (#185C33)
- Minimal box shadows
- 4px border radius

### Alerts
- Subtle background colors (5-10% opacity)
- 3px left border in appropriate color
- No bright backgrounds

### Metrics/Cards
- White background
- Light grey border (#e0e0e0)
- Subtle shadow: `0 1px 3px rgba(0,0,0,0.1)`
- 6px border radius

## Layout Guidelines

### Spacing
- Section padding: 2rem
- Component margins: 1-2rem
- Consistent spacing throughout

### Maximum Width
- Main content: 1200px
- Center-aligned with auto margins

### Responsive Design
- Mobile-first approach
- Flexible grid layouts
- Appropriate breakpoints

## Do's and Don'ts

### Do's ✅
- Use UVU Green as the dominant color
- Maintain plenty of white space
- Keep designs clean and minimal
- Use grey for subtle elements
- Follow the 80/15/5 color ratio

### Don'ts ❌
- Don't use bright gradients
- Don't overuse accent colors
- Don't add unnecessary animations
- Don't use multiple colors in one element
- Don't create busy or cluttered layouts

## Implementation Notes

### Streamlit Configuration
The application uses:
1. Custom CSS injection for consistent styling
2. Streamlit theme configuration (`.streamlit/config.toml`)
3. Component-level styling where needed

### Accessibility
- Maintain WCAG AA contrast ratios
- Use semantic HTML where possible
- Provide clear focus states
- Ensure readable font sizes

## Future Considerations
- Consider implementing a dark mode with appropriate UVU colors
- Explore custom Streamlit components for better brand control
- Regular reviews to ensure continued alignment with UVU brand updates

---

*Last Updated: [Current Date]*
*Based on Utah Valley University Brand Guidelines*
