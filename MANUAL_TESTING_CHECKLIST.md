# Manual Frontend Testing Checklist

**URL:** http://localhost:3000  
**Backend:** http://localhost:8000 (must be running)

---

## Pre-Test Setup

- [ ] Backend server is running (`cd backend && source venv/bin/activate && uvicorn main:app --reload`)
- [ ] Frontend server is running (`cd frontend && npm run dev`)
- [ ] Browser is open to http://localhost:3000

---

## Test 11: Message Display ✅

**Objective:** Verify message bubbles display correctly

### Steps:
1. Type "Hello" and send
2. Wait for response

### Expected Results:
- [ ] User message appears on the right side
- [ ] User message has blue background
- [ ] Assistant message appears on the left side
- [ ] Assistant message has gray/white background
- [ ] Text is readable and properly formatted
- [ ] Messages have proper spacing

**Status:** _________

---

## Test 12: Agent Identification ✅

**Objective:** Verify agent badges display correctly for each agent type

### Steps:
1. Send: "What does the Enterprise plan cost?"
   - [ ] **Expected:** 💰 Billing badge (blue)
   
2. Send: "My API keeps timing out, how do I fix it?"
   - [ ] **Expected:** 🔧 Technical Support badge (orange)
   
3. Send: "Do you comply with GDPR?"
   - [ ] **Expected:** 📋 Policy & Compliance badge (green)

### Expected Results:
- [ ] Each agent badge shows correct emoji
- [ ] Each agent badge shows correct label
- [ ] Each agent badge has distinct color
- [ ] Badges appear at the top of assistant messages

**Status:** _________

---

## Test 13: Real-Time Streaming Display ✅

**Objective:** Verify tokens stream smoothly in real-time

### Steps:
1. Send: "Explain your refund policy in detail"
2. Watch the response appear

### Expected Results:
- [ ] "AI is thinking..." indicator appears first
- [ ] Response appears word-by-word (not all at once)
- [ ] Streaming is smooth without jarring jumps
- [ ] No lag or stuttering
- [ ] Response feels natural and real-time

**Status:** _________

---

## Test 14: Input State Management ✅

**Objective:** Verify input field behaves correctly

### Steps:
1. Type a message in the input field
2. Click Send button
3. Observe input field during response

### Expected Results:
- [ ] Input field clears immediately after sending
- [ ] Input field is disabled (grayed out) while waiting for response
- [ ] Send button is disabled while waiting
- [ ] Placeholder changes to "Please wait..." during processing
- [ ] Input re-enables after response completes
- [ ] Can type new message after response

**Status:** _________

---

## Test 15: Auto-Scroll ✅

**Objective:** Verify conversation auto-scrolls to show latest messages

### Steps:
1. Send 3-4 messages to build up conversation history
2. Observe scrolling behavior

### Expected Results:
- [ ] View automatically scrolls to show latest message
- [ ] Scrolling is smooth (not jarring)
- [ ] Works for both user and assistant messages
- [ ] Latest message is always visible

**Status:** _________

---

## Test 16: Error Display ✅

**Objective:** Verify error handling and display

### Steps:
1. Stop the backend server (Ctrl+C in backend terminal)
2. Try sending a message in the frontend
3. Observe error display
4. Restart backend server
5. Click "Try Again" button

### Expected Results:
- [ ] Error message displays in red box
- [ ] Error message is user-friendly (not technical)
- [ ] Warning emoji ⚠️ appears
- [ ] "Try Again" button is visible
- [ ] Clicking retry resends the message
- [ ] After backend restarts, retry works correctly

**Status:** _________

---

## Test 17: Session Persistence ✅

**Objective:** Verify session maintains conversation history

### Steps:
1. Note the session ID in the header (e.g., "Session: a5b20b5b...")
2. Send: "What are your pricing plans?"
3. Send: "Can I upgrade?"
4. Send: "What about downgrades?"
5. Scroll up to see all messages

### Expected Results:
- [ ] Session ID remains the same across all messages
- [ ] All messages remain visible in the conversation
- [ ] Message history is maintained
- [ ] Can scroll up to see previous messages

**Status:** _________

---

## Test 18: End-to-End Flow ✅

**Objective:** Verify complete user journey with agent switching

### Steps:
1. Start with billing: "How much does the Premium plan cost?"
   - Wait for response, verify 💰 Billing badge
   
2. Switch to technical: "I'm having login issues"
   - Wait for response, verify 🔧 Technical badge
   
3. Switch to policy: "What's your privacy policy?"
   - Wait for response, verify 📋 Policy badge
   
4. Follow-up: "Does that apply to EU citizens?"
   - Wait for response, verify stays with 📋 Policy

### Expected Results:
- [ ] Each query routes to correct agent
- [ ] Agent badges switch appropriately
- [ ] Responses are relevant to the query type
- [ ] Experience is seamless
- [ ] No errors or glitches
- [ ] Session ID remains consistent

**Status:** _________

---

## Test 20: Cold Start (Backend Restart) ✅

**Objective:** Verify system recovers after restart

### Steps:
1. Stop backend server (Ctrl+C)
2. Wait 5 seconds
3. Restart backend server
4. In frontend, send: "Test message"

### Expected Results:
- [ ] Backend startup logs show ChromaDB loading
- [ ] Backend shows "126 documents" loaded
- [ ] Frontend message sends successfully
- [ ] Response is received correctly
- [ ] No errors in either console

**Status:** _________

---

## Additional UI/UX Checks

### Welcome Screen
- [ ] Shows on first load
- [ ] Has 💬 emoji and title
- [ ] Shows three agent cards (Billing, Technical, Policy)
- [ ] Agent cards have correct colors and descriptions

### Dark Mode (if system is in dark mode)
- [ ] All text is readable
- [ ] Colors are appropriate for dark theme
- [ ] Agent badges look good
- [ ] No contrast issues

### Responsive Design
- [ ] Resize browser window to mobile size
- [ ] Messages still display correctly
- [ ] Input field is usable
- [ ] Agent cards stack vertically

### Keyboard Shortcuts
- [ ] Enter key sends message
- [ ] Shift+Enter creates new line in input
- [ ] Help text shows keyboard shortcuts

---

## Summary

**Total Tests:** 10 core tests + 4 additional checks  
**Tests Passed:** _____ / 14  
**Tests Failed:** _____ / 14  
**Success Rate:** _____%

### Issues Found:
1. _______________________________________________________
2. _______________________________________________________
3. _______________________________________________________

### Overall Assessment:
- [ ] **Excellent** - All tests passed, no issues
- [ ] **Good** - Minor cosmetic issues only
- [ ] **Acceptable** - Some issues but system functional
- [ ] **Needs Work** - Major issues found

---

## Notes

_Add any additional observations, suggestions, or feedback here:_

________________________________________________________________________
________________________________________________________________________
________________________________________________________________________

---

**Tested By:** ___________________  
**Date:** ___________________  
**Time Spent:** ___________ minutes  
**Browser:** ___________________


