# Design: Admin Partial Tab Navigation Scroll Reset

**Issue:** #3748
**Date:** 2026-03-30
**Status:** Approved

## Problem Statement

When switching between admin sidebar tabs that load partial content (MCP Servers, Tools, Virtual Servers, etc.), the main content area retains the previous scroll position instead of resetting to the top. This creates a poor user experience where users must manually scroll up to see the beginning of newly loaded content.

### Current Behavior
1. User opens "MCP Servers" tab
2. User scrolls to the bottom of the page
3. User clicks "Tools" tab
4. Tools view loads at the old scroll offset (bottom of page)
5. User must manually scroll to top

### Expected Behavior
The main content area should reset to the top whenever the user switches to a different admin sidebar section.

## Root Cause

The `showTab()` function in `mcpgateway/static/admin.js` (lines 8712-9282) handles tab switching by:
- Hiding all panels
- Revealing the target panel
- Updating active states
- Triggering content loads

However, it does not reset the scroll position of the scrollable container (`<main>` element with class `overflow-y-auto` at line 1006 in `admin.html`). Since HTMX partial loads update content without full page reloads, the browser maintains the scroll position of the container.

## Architecture

### Component Affected
**File:** `mcpgateway/static/admin.js`
**Function:** `showTab(tabName)`
**Location:** Lines 8712-9282

### Scrollable Container
**File:** `mcpgateway/templates/admin.html`
**Element:** `<main class="flex-1 overflow-y-auto bg-gray-100 dark:bg-gray-900 p-4 lg:p-6">`
**Location:** Line 1006

This `<main>` element is the actual scrollable container for all admin content. Individual panels are not scrollable; they are children of this scrolling container.

## Solution: Approach 1 - Reset Scroll on Main Content Element

### Implementation

Add scroll reset logic in the `showTab()` function immediately after revealing the chosen panel (around line 8805).

**Code Change:**
```javascript
// Reveal chosen panel
const panel = safeGetElement(`${tabName}-panel`);
if (panel) {
    panel.classList.remove("hidden");

    // Reset scroll position on the main content area
    const mainContent = document.querySelector('main.overflow-y-auto');
    if (mainContent) {
        mainContent.scrollTop = 0;
    }
} else {
    console.error(`Panel ${tabName}-panel not found`);
    const fallbackTab = getDefaultTabName();
    if (fallbackTab && fallbackTab !== tabName) {
        updateHashForTab(fallbackTab);
        showTab(fallbackTab);
    }
    return;
}
```

### Why This Works

1. **Targets the correct element** - The `<main>` element with `overflow-y-auto` is the scrollable container
2. **Synchronous execution** - `scrollTop = 0` executes immediately, before the user sees the new content
3. **Uses existing utilities** - Leverages `querySelector` with the specific class for precision
4. **Safe** - Includes null check to prevent errors if DOM structure changes
5. **Minimal change** - Single focused addition to existing logic

### Timing

The scroll reset happens:
1. After all panels are hidden
2. After the target panel is revealed
3. Before debounced content loading (300ms delay)
4. Synchronously, so no visual "jump" occurs

## Alternatives Considered

### Approach 2: Reset scroll using window.scrollTo
```javascript
window.scrollTo(0, 0);
```

**Rejected because:**
- The scrollable element is the `<main>` container, not the window
- Less precise targeting
- May not work correctly in all viewport configurations

### Approach 3: Scroll each panel individually

**Rejected because:**
- Requires changes in multiple locations
- Panels themselves aren't scrollable - the `<main>` container is
- More complex and harder to maintain

## Error Handling

### Built-in Safety
1. **Null check on mainContent** - If the DOM structure changes and the element isn't found, code safely skips scroll reset
2. **Existing try-catch** - The `showTab()` function already has comprehensive error handling
3. **Graceful degradation** - If scroll reset fails, tab switch still completes; only side effect is scroll position isn't reset (current behavior)

### No New Error Cases
This is a low-risk addition. The scroll reset is an enhancement that fails safely if the target element isn't found.

## Testing Strategy

### Manual Testing
1. Start admin UI with `make dev`
2. Navigate to "MCP Servers" tab
3. Scroll to the bottom of the page
4. Click "Tools" in the sidebar
5. **Verify:** Tools view appears at the top (scrollTop = 0)
6. Repeat for other tab combinations:
   - MCP Servers → Virtual Servers
   - Virtual Servers → Resources
   - Resources → Prompts
   - Prompts → Tools
   - Any tab → Overview

### Expected Behavior
- Every tab switch starts at the top of the content area
- No visual "jump" or delay - scroll reset is immediate
- Smooth user experience

### Edge Cases
1. **Rapid tab switching** - Verify debounce doesn't interfere with scroll reset
2. **Already active tab** - Should be no-op per existing idempotency check (lines 8745-8759)
3. **Sidebar collapsed/expanded** - Scroll reset works in both states
4. **Mobile viewport** - Works with mobile menu overlay
5. **Hidden tabs** - Fallback logic doesn't break scroll reset

### Automated Testing
The codebase has Playwright tests (referenced in git history commits like #3370). If UI tests exist for tab navigation, they should continue to pass. The scroll reset is an enhancement to existing behavior, not a breaking change.

If specific scroll position tests exist, they may need updating to expect `scrollTop = 0` after tab switches.

## Implementation Checklist

- [ ] Modify `showTab()` function in `mcpgateway/static/admin.js`
- [ ] Add scroll reset code after panel reveal (around line 8805)
- [ ] Test all admin sidebar tabs
- [ ] Test edge cases (rapid switching, mobile, collapsed sidebar)
- [ ] Verify no console errors
- [ ] Check Playwright tests still pass
- [ ] Update tests if needed

## Impact Assessment

### Files Modified
- `mcpgateway/static/admin.js` - 4 lines added

### Scope
- Affects all admin sidebar navigation
- No breaking changes
- No database migrations
- No API changes
- Client-side only

### Risk Level
**Low** - Small, focused change with graceful failure mode

### User Experience Impact
**Positive** - Resolves frustrating UX issue where users had to manually scroll to top after every tab switch

## Success Criteria

1. ✅ Scroll position resets to top on every tab switch
2. ✅ No visual artifacts or delays
3. ✅ Works across all admin tabs
4. ✅ No console errors
5. ✅ Existing tests pass
6. ✅ Works on mobile and desktop viewports
