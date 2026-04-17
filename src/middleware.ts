import { defineMiddleware } from 'astro:middleware';

// WP post ID → new URL map
const WP_P_MAP: Record<string, string> = {
  '4383': '/skin-and-hair-conditions/',
  '4595': '/skin-and-hair-conditions/',
  '4663': '/alopecia-hair-loss/',
  '4668': '/pigmentation-issues/',
  '4725': '/product-reviews/',
  '4761': '/find-a-practitioner/',
  '4991': '/community-products/tell-us-about-a-product/',
  '4993': '/community-products/ask-us-to-review-a-product/',
  '5253': '/expertvoices/',
  '5368': '/informative/laser-treatment-for-acne-scars/',
  '5390': '/informative/chemical-peels/',
  '5408': '/informative/causes-of-acne-in-skin-of-color-options-to-address-it/',
  '5444': '/informative/fragile-hair/',
  '5449': '/informative/treatments-for-central-centrifugal-cicatricial-alopecia-ccca/',
  '5467': '/informative/hair-disorders-in-black-women/',
  '5487': '/informative/melanin-what-gives-our-skin-its-color/',
  '5517': '/informative/melasma-a-common-hyperpigmentation-disorder/',
  '5530': '/informative/how-to-choose-your-dermatologist/',
  '5574': '/community-conversations/',
  '5578': '/informative/if-you-use-hair-straighteners-or-relaxers-you-must-read-this/',
  '6285': '/informative/the-importance-of-a-healthy-skin/',
  '6287': '/informative/dermatology-for-black-women/',
  '6373': '/join-us/',
  '7167': '/informative/common-skin-and-hair-conditions/',
  '7469': '/meet-our-experts/',
  '7897': '/privacy-policy/',
  '8107': '/care/',
  '8138': '/informative/why-is-black-skin-more-likely-to-itch/',
  '8150': '/informative/botox-and-dermal-fillers-for-black-women/',
  '8162': '/informative/permanent-makeup-and-tattoos-in-black-women/',
  '8289': '/who/',
  '8338': '/advocacy/',
  '8353': '/michelleyoung/',
  '8447': '/chesahna-kindred/',
  '8475': '/steve-kirnon/',
  '8494': '/amy-mcmichael/',
  '8511': '/ginette-okoye/',
  '8516': '/karen-semien-mcbride/',
  '8751': '/telehealth/',
  '9059': '/advocacy2/',
  '9115': '/telehealth/california-coming-july-2025/',
  '9140': '/telehealth/maryland-coming-july-2025/',
  '9298': '/informative/what-you-need-to-know-about-seborrheic-dermatitis/',
  '9365': '/informative/what-you-need-to-know-about-seborrheic-dermatitis-3-min-read/',
  '9374': '/informative/what-you-need-to-know-about-seborrheic-dermatitis/',
};

export const onRequest = defineMiddleware((context, next) => {
  const p = context.url.searchParams.get('p');
  if (p && WP_P_MAP[p]) {
    return context.redirect(WP_P_MAP[p], 301);
  }
  return next();
});
