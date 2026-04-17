import { config, fields, collection, singleton } from '@keystatic/core';

const richText = fields.document({
  label: 'Body',
  formatting: true,
  dividers: true,
  links: true,
  images: {
    directory: 'public/content-images',
    publicPath: '/content-images/',
  },
  tables: true,
});

const seo = fields.object({
  metaTitle: fields.text({ label: 'Meta title (optional)' }),
  metaDescription: fields.text({ label: 'Meta description', multiline: true }),
  ogImage: fields.image({
    label: 'Social share image',
    directory: 'public/content-images/og',
    publicPath: '/content-images/og/',
  }),
});

const ctaBlock = fields.object({
  label: fields.text({ label: 'CTA label' }),
  href: fields.text({ label: 'CTA link' }),
});

export default config({
  storage:
    process.env.NODE_ENV === 'production'
      ? {
          kind: 'github',
          repo: { owner: 'josepc', name: 'weseecolor' },
        }
      : { kind: 'local' },

  ui: {
    brand: { name: 'WeSeeColor' },
    navigation: {
      Content: ['articles', 'experts', 'videos', 'resources', 'hubs'],
      Pages: ['home', 'whoWeAre', 'advocacy', 'privacyPolicy', 'care', 'communityConversations', 'expertVoices', 'productReviews', 'joinUs', 'telehealth', 'findAPractitioner', 'askUsToReviewAProduct', 'tellUsAboutAProduct'],
      Settings: ['settings', 'navigation', 'footer'],
    },
  },

  collections: {
    articles: collection({
      label: 'Articles',
      slugField: 'slug',
      path: 'src/content/articles/*',
      format: { contentField: 'body' },
      entryLayout: 'content',
      columns: ['title', 'category', 'publishedAt'],
      schema: {
        title: fields.text({ label: 'Title', validation: { isRequired: true } }),
        slug: fields.text({ label: 'URL slug (dated)', description: 'e.g. 2024-01-24-melasma-a-common-hyperpigmentation-disorder' }),
        publishedAt: fields.date({ label: 'Published', defaultValue: { kind: 'today' } }),
        readTime: fields.text({ label: 'Read time (e.g. 3 min)' }),
        category: fields.select({
          label: 'Category',
          options: [
            { label: 'Skin Care', value: 'skin-care' },
            { label: 'Hair Care', value: 'hair-care' },
            { label: 'Science', value: 'science' },
            { label: 'Education', value: 'education' },
            { label: 'Conditions', value: 'conditions' },
            { label: 'Community', value: 'community' },
          ],
          defaultValue: 'education',
        }),
        excerpt: fields.text({ label: 'Excerpt', multiline: true }),
        coverImage: fields.image({
          label: 'Cover image',
          directory: 'public/content-images/articles',
          publicPath: '/content-images/articles/',
        }),
        tags: fields.array(fields.text({ label: 'Tag' }), { label: 'Tags', itemLabel: (p) => p.value }),
        authors: fields.array(
          fields.relationship({ label: 'Author', collection: 'experts' }),
          { label: 'Authors', itemLabel: (p) => p.value ?? '—' },
        ),
        body: richText,
        sources: fields.array(
          fields.object({
            label: fields.text({ label: 'Label' }),
            url: fields.url({ label: 'URL' }),
          }),
          { label: 'Sources / references', itemLabel: (p) => p.fields.label.value },
        ),
        seo,
      },
    }),

    experts: collection({
      label: 'Expert profiles',
      slugField: 'slug',
      path: 'src/content/experts/*',
      format: { contentField: 'bio' },
      columns: ['name', 'role'],
      schema: {
        slug: fields.text({
          label: 'URL slug',
          description: 'Matches live URL, e.g. amy-mcmichael, michelleyoung',
        }),
        name: fields.text({ label: 'Name', validation: { isRequired: true } }),
        credentials: fields.text({ label: 'Credentials (e.g. MD, PhD)' }),
        role: fields.text({ label: 'Role / title' }),
        photo: fields.image({
          label: 'Photo',
          directory: 'public/content-images/experts',
          publicPath: '/content-images/experts/',
        }),
        expertise: fields.array(fields.text({ label: 'Area' }), { label: 'Expertise', itemLabel: (p) => p.value }),
        links: fields.array(
          fields.object({
            label: fields.text({ label: 'Label' }),
            url: fields.url({ label: 'URL' }),
          }),
          { label: 'Links', itemLabel: (p) => p.fields.label.value },
        ),
        featuredVideoUrl: fields.url({ label: 'Featured video (YouTube URL)' }),
        order: fields.integer({ label: 'Sort order', defaultValue: 0 }),
        bio: richText,
        seo,
      },
    }),

    videos: collection({
      label: 'Videos',
      slugField: 'title',
      path: 'src/content/videos/*',
      columns: ['title', 'category'],
      schema: {
        title: fields.text({ label: 'Title', validation: { isRequired: true } }),
        youtubeUrl: fields.url({ label: 'YouTube URL' }),
        description: fields.text({ label: 'Description', multiline: true }),
        category: fields.select({
          label: 'Category',
          options: [
            { label: 'Expert Voices', value: 'expert-voices' },
            { label: 'Conditions', value: 'conditions' },
            { label: 'Community', value: 'community' },
            { label: 'Education', value: 'education' },
          ],
          defaultValue: 'expert-voices',
        }),
        thumbnail: fields.image({
          label: 'Custom thumbnail (optional)',
          directory: 'public/content-images/videos',
          publicPath: '/content-images/videos/',
        }),
        publishedAt: fields.date({ label: 'Published', defaultValue: { kind: 'today' } }),
      },
    }),

    resources: collection({
      label: 'Resources',
      slugField: 'title',
      path: 'src/content/resources/*',
      schema: {
        title: fields.text({ label: 'Title', validation: { isRequired: true } }),
        description: fields.text({ label: 'Description', multiline: true }),
        link: fields.url({ label: 'External link' }),
        category: fields.text({ label: 'Category' }),
        thumbnail: fields.image({
          label: 'Thumbnail',
          directory: 'public/content-images/resources',
          publicPath: '/content-images/resources/',
        }),
      },
    }),

    hubs: collection({
      label: 'Hub / Condition pages',
      slugField: 'slug',
      path: 'src/content/hubs/*',
      format: { contentField: 'intro' },
      columns: ['title', 'slug'],
      schema: {
        slug: fields.text({
          label: 'URL slug',
          description: 'e.g. seborrheic-dermatitis, skin-and-hair-conditions',
        }),
        title: fields.text({ label: 'Title', validation: { isRequired: true } }),
        heroImage: fields.image({
          label: 'Hero image',
          directory: 'public/content-images/hubs',
          publicPath: '/content-images/hubs/',
        }),
        intro: richText,
        videoRefs: fields.array(
          fields.relationship({ label: 'Video', collection: 'videos' }),
          { label: 'Videos in this hub', itemLabel: (p) => p.value ?? '—' },
        ),
        articleRefs: fields.array(
          fields.relationship({ label: 'Article', collection: 'articles' }),
          { label: 'Related articles', itemLabel: (p) => p.value ?? '—' },
        ),
        externalLinks: fields.array(
          fields.object({
            label: fields.text({ label: 'Label' }),
            url: fields.url({ label: 'URL' }),
          }),
          { label: 'External links', itemLabel: (p) => p.fields.label.value },
        ),
        seo,
      },
    }),
  },

  singletons: {
    home: singleton({
      label: 'Home page',
      path: 'src/content/pages/home',
      format: { data: 'json' },
      schema: {
        title: fields.text({ label: 'Page title', defaultValue: 'WeSeeColor' }),
        heroSlides: fields.array(
          fields.object({
            image: fields.image({
              label: 'Image',
              directory: 'public/content-images/hero',
              publicPath: '/content-images/hero/',
            }),
            eyebrow: fields.text({ label: 'Eyebrow' }),
            headline: fields.text({ label: 'Headline' }),
            sub: fields.text({ label: 'Sub', multiline: true }),
            cta: ctaBlock,
          }),
          { label: 'Hero slides', itemLabel: (p) => p.fields.headline.value || 'Slide' },
        ),
        featuredArticles: fields.array(
          fields.relationship({ label: 'Article', collection: 'articles' }),
          { label: 'Featured articles', itemLabel: (p) => p.value ?? '—' },
        ),
        featuredVideos: fields.array(
          fields.relationship({ label: 'Video', collection: 'videos' }),
          { label: 'Featured videos', itemLabel: (p) => p.value ?? '—' },
        ),
        featuredExperts: fields.array(
          fields.relationship({ label: 'Expert', collection: 'experts' }),
          { label: 'Featured experts', itemLabel: (p) => p.value ?? '—' },
        ),
        ctaBlock: fields.object({
          eyebrow: fields.text({ label: 'Eyebrow' }),
          heading: fields.text({ label: 'Heading' }),
          body: fields.text({ label: 'Body', multiline: true }),
          primaryCta: ctaBlock,
          secondaryCta: ctaBlock,
        }),
        seo,
      },
    }),

    whoWeAre: singleton({
      label: 'Who We Are',
      path: 'src/content/pages/who',
      format: { contentField: 'body' },
      schema: {
        title: fields.text({ label: 'Title', defaultValue: 'Who We Are' }),
        heroImage: fields.image({
          label: 'Hero image',
          directory: 'public/content-images/pages',
          publicPath: '/content-images/pages/',
        }),
        body: richText,
        seo,
      },
    }),

    advocacy: singleton({
      label: 'Advocacy',
      path: 'src/content/pages/advocacy',
      format: { contentField: 'body' },
      schema: {
        title: fields.text({ label: 'Title', defaultValue: 'Advocacy' }),
        heroImage: fields.image({
          label: 'Hero image',
          directory: 'public/content-images/pages',
          publicPath: '/content-images/pages/',
        }),
        body: richText,
        seo,
      },
    }),

    privacyPolicy: singleton({
      label: 'Privacy Policy',
      path: 'src/content/pages/privacy-policy',
      format: { contentField: 'body' },
      schema: {
        title: fields.text({ label: 'Title', defaultValue: 'Privacy Policy' }),
        body: richText,
        seo,
      },
    }),

    care: singleton({
      label: 'Care hub',
      path: 'src/content/pages/care',
      format: { contentField: 'body' },
      schema: {
        title: fields.text({ label: 'Title', defaultValue: 'Care' }),
        heroImage: fields.image({
          label: 'Hero image',
          directory: 'public/content-images/pages',
          publicPath: '/content-images/pages/',
        }),
        body: richText,
        seo,
      },
    }),

    communityConversations: singleton({
      label: 'Community Conversations',
      path: 'src/content/pages/community-conversations',
      format: { contentField: 'body' },
      schema: {
        title: fields.text({ label: 'Title', defaultValue: 'Community Conversations' }),
        heroImage: fields.image({
          label: 'Hero image',
          directory: 'public/content-images/pages',
          publicPath: '/content-images/pages/',
        }),
        body: richText,
        seo,
      },
    }),

    expertVoices: singleton({
      label: 'Expert Voices hub',
      path: 'src/content/pages/expert-voices',
      format: { contentField: 'body' },
      schema: {
        title: fields.text({ label: 'Title', defaultValue: 'Expert Voices' }),
        heroImage: fields.image({
          label: 'Hero image',
          directory: 'public/content-images/pages',
          publicPath: '/content-images/pages/',
        }),
        body: richText,
        featuredVideos: fields.array(
          fields.relationship({ label: 'Video', collection: 'videos' }),
          { label: 'Featured videos', itemLabel: (p) => p.value ?? '—' },
        ),
        seo,
      },
    }),

    productReviews: singleton({
      label: 'Product Reviews',
      path: 'src/content/pages/product-reviews',
      format: { contentField: 'body' },
      schema: {
        title: fields.text({ label: 'Title', defaultValue: 'Product Reviews' }),
        heroImage: fields.image({
          label: 'Hero image',
          directory: 'public/content-images/pages',
          publicPath: '/content-images/pages/',
        }),
        body: richText,
        seo,
      },
    }),

    joinUs: singleton({
      label: 'Join Us',
      path: 'src/content/pages/join-us',
      format: { contentField: 'body' },
      schema: {
        title: fields.text({ label: 'Title', defaultValue: 'Join Us' }),
        body: richText,
        seo,
      },
    }),

    telehealth: singleton({
      label: 'Telehealth',
      path: 'src/content/pages/telehealth',
      format: { contentField: 'body' },
      schema: {
        title: fields.text({ label: 'Title', defaultValue: 'Telehealth' }),
        heroImage: fields.image({
          label: 'Hero image',
          directory: 'public/content-images/pages',
          publicPath: '/content-images/pages/',
        }),
        body: richText,
        seo,
      },
    }),

    findAPractitioner: singleton({
      label: 'Find a Practitioner',
      path: 'src/content/pages/find-a-practitioner',
      format: { contentField: 'body' },
      schema: {
        title: fields.text({ label: 'Title', defaultValue: 'Find a Practitioner' }),
        intro: richText,
        body: richText,
        tallyFormId: fields.text({ label: 'Tally form ID for this page' }),
        seo,
      },
    }),

    askUsToReviewAProduct: singleton({
      label: 'Ask Us to Review a Product',
      path: 'src/content/pages/ask-us-to-review-a-product',
      format: { contentField: 'body' },
      schema: {
        title: fields.text({ label: 'Title', defaultValue: 'Ask Us to Review a Product' }),
        body: richText,
        tallyFormId: fields.text({ label: 'Tally form ID for this page' }),
        seo,
      },
    }),

    tellUsAboutAProduct: singleton({
      label: 'Tell Us About a Product',
      path: 'src/content/pages/tell-us-about-a-product',
      format: { contentField: 'body' },
      schema: {
        title: fields.text({ label: 'Title', defaultValue: 'Tell Us About a Product' }),
        body: richText,
        tallyFormId: fields.text({ label: 'Tally form ID for this page' }),
        seo,
      },
    }),

    settings: singleton({
      label: 'Site settings',
      path: 'src/content/settings/site',
      format: { data: 'json' },
      schema: {
        siteTitle: fields.text({ label: 'Site title', defaultValue: 'WeSeeColor' }),
        siteDescription: fields.text({ label: 'Site description', multiline: true }),
        defaultOgImage: fields.image({
          label: 'Default OG image',
          directory: 'public/content-images/og',
          publicPath: '/content-images/og/',
        }),
        tallyFormIds: fields.object({
          productEvaluationRequest: fields.text({ label: 'Product evaluation request form ID' }),
          tellUsAboutAProduct: fields.text({ label: 'Tell us about a product form ID' }),
          findAPractitioner: fields.text({ label: 'Find a practitioner form ID' }),
        }),
        analyticsId: fields.text({ label: 'Analytics site ID (Plausible/CF Web Analytics)' }),
      },
    }),

    navigation: singleton({
      label: 'Main navigation',
      path: 'src/content/settings/navigation',
      format: { data: 'json' },
      schema: {
        items: fields.array(
          fields.object({
            label: fields.text({ label: 'Label' }),
            href: fields.text({ label: 'URL' }),
            children: fields.array(
              fields.object({
                label: fields.text({ label: 'Label' }),
                href: fields.text({ label: 'URL' }),
              }),
              { label: 'Children', itemLabel: (p) => p.fields.label.value },
            ),
          }),
          { label: 'Nav items', itemLabel: (p) => p.fields.label.value },
        ),
      },
    }),

    footer: singleton({
      label: 'Footer',
      path: 'src/content/settings/footer',
      format: { data: 'json' },
      schema: {
        columns: fields.array(
          fields.object({
            title: fields.text({ label: 'Column title' }),
            links: fields.array(
              fields.object({
                label: fields.text({ label: 'Label' }),
                href: fields.text({ label: 'URL' }),
              }),
              { label: 'Links', itemLabel: (p) => p.fields.label.value },
            ),
          }),
          { label: 'Columns', itemLabel: (p) => p.fields.title.value },
        ),
        social: fields.array(
          fields.object({
            platform: fields.text({ label: 'Platform' }),
            url: fields.url({ label: 'URL' }),
          }),
          { label: 'Social links', itemLabel: (p) => p.fields.platform.value },
        ),
        copyright: fields.text({ label: 'Copyright line' }),
      },
    }),
  },
});
