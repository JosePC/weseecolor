# Tally Forms Specification

Three Tally forms power the interactive features on WeSeeColor. Create them at tally.so, then paste the form IDs into **Keystatic → Settings → Tally Form IDs**.

---

## 1. Find a Practitioner

**Page:** `/find-a-practitioner/`  
**Keystatic field:** `settings.tallyFormIds.findAPractitioner`

### Fields

| Label | Type | Required | Notes |
|---|---|---|---|
| State / Region | Dropdown | Yes | All 50 US states + DC |
| Skin or hair condition | Dropdown | Yes | Options: Acne, Alopecia / Hair Loss, Pigmentation / Melasma, Seborrheic Dermatitis, Eczema, Other |
| Insurance preference | Multiple choice | No | Options: Accepts insurance, Self-pay OK, Either |
| Your email address | Email | Yes | For follow-up referral |
| May we contact you? | Checkbox | Yes | Consent to receive practitioner referral by email |

### Conditional logic

- If **State** = California → show message: "WeSeeColor telehealth is coming to California in July 2025. [Check back here](/telehealth/california-coming-july-2025/)" and hide submit button.
- If **State** = Maryland → same message but link to Maryland coming-soon page.
- If **State** is any other state not yet served → redirect to `/telehealth/state-not-available/` or show inline message.

### Email confirmation (to submitter)

> **Subject:** Your WeSeeColor practitioner request
>
> Thank you for reaching out! We received your request for a dermatologist who specializes in Black skin and hair in **{State}**.
>
> We'll review your information and follow up within 5–7 business days with recommendations.
>
> — The WeSeeColor Team

---

## 2. Ask Us to Review a Product

**Page:** `/community-products/ask-us-to-review-a-product/`  
**Keystatic field:** `settings.tallyFormIds.productEvaluationRequest`

### Fields

| Label | Type | Required | Notes |
|---|---|---|---|
| Product name | Short text | Yes | |
| Brand name | Short text | Yes | |
| Product type / category | Dropdown | Yes | Options: Moisturizer, Cleanser, Sunscreen, Hair care, Styling product, Treatment / serum, Makeup, Other |
| Where can this product be purchased? | Short text | No | URL or store name |
| Why should we review this product? | Long text | Yes | Min 50 chars |
| Has this product received media attention or gone viral? | Multiple choice | No | Options: Yes, No, Not sure |
| Your name (optional) | Short text | No | |
| Your email (optional) | Email | No | To notify when review is published |
| I understand this is a community request and does not guarantee a review. | Checkbox | Yes | Consent |

### Conditional logic

- If **Product type** = Other → show free-text field: "Please describe the product type."
- If **email** is provided → show opt-in: "Notify me when this review is published."

### Email confirmation (if email provided)

> **Subject:** We received your product review request
>
> Thanks for submitting **{Product name}** by **{Brand name}** for consideration.
>
> Our expert panel reviews community requests on a rolling basis. If we publish an analysis of this product, we'll send you a link.
>
> — WeSeeColor

---

## 3. Tell Us About a Product

**Page:** `/community-products/tell-us-about-a-product/`  
**Keystatic field:** `settings.tallyFormIds.tellUsAboutAProduct`

### Purpose

Shorter, lower-friction form for community members to flag products — positive or negative — they've encountered. No expert review promised.

### Fields

| Label | Type | Required | Notes |
|---|---|---|---|
| Product name | Short text | Yes | |
| Brand name | Short text | Yes | |
| Product category | Dropdown | Yes | Same options as form 2 |
| Your experience with this product | Multiple choice | Yes | Options: Positive, Negative, Mixed, Haven't tried it but seen it recommended |
| Tell us more (optional) | Long text | No | |
| Where did you find this product? | Short text | No | e.g. TikTok, CVS, a friend |
| Your email (optional) | Email | No | |
| I agree to WeSeeColor's [privacy policy](/privacy-policy/). | Checkbox | Yes | |

### Conditional logic

- If **experience** = Negative → show follow-up: "Did you experience any adverse reactions? (Optional)" — long text field.
- If **experience** = Positive → show follow-up: "What did you love about it?" — long text field.

### Email confirmation (if email provided)

> **Subject:** Thanks for sharing!
>
> We received your tip about **{Product name}**. Community input like yours helps us prioritize what to review next.
>
> — WeSeeColor

---

## Setup checklist

1. Create all three forms at [tally.so](https://tally.so).
2. Set each form's **redirect** or **close message** as appropriate.
3. Enable **email notifications** (to `hello@weseecolor.net` or team inbox) for all submissions.
4. Copy the form IDs (e.g. `wMdYkP`) from the Tally share URL.
5. In Keystatic → Settings → Tally Form IDs, paste the IDs into the three fields.
6. Test each embed on the live site.
