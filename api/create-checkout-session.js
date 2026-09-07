// api/create-checkout-session.js
// Vercel Serverless Function — Uko UI Stripe Checkout

const PRICE_IDS = {
  starter: 'price_1U9YoM15gAppL16WabQvpP1n',
  pro:     'price_1U9YoM15gAppL16W4heWCLLG',
};

const MASCOT_NAMES = {
  aituko: 'AItuko',
  owluko: 'Owluko',
  luneko: 'Luneko',
  hatoko: 'Hatoko',
  usako:  'Usako',
};

export default async function handler(req, res) {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { tier, mascot, email, origin } = req.body || {};

  // Validation
  if (!tier || !PRICE_IDS[tier]) {
    return res.status(400).json({ error: 'Invalid tier. Must be "starter" or "pro".' });
  }
  if (!mascot || !MASCOT_NAMES[mascot]) {
    return res.status(400).json({ error: 'Invalid mascot. Must be "aituko", "owluko", or "luneko".' });
  }

  const baseUrl = origin || `https://${req.headers.host}`;
  const mascotName = MASCOT_NAMES[mascot];
  const tierLabel = tier === 'pro' ? 'Pack Pro (12 États)' : 'Pack Essentiel (Starter)';

  try {
    const stripe = (await import('stripe')).default(process.env.STRIPE_SECRET_KEY);

    const sessionParams = {
      mode: 'payment',
      payment_method_types: ['card'],
      line_items: [
        {
          price: PRICE_IDS[tier],
          quantity: 1,
          adjustable_quantity: { enabled: false },
        },
      ],
      customer_email: email || undefined,
      metadata: {
        mascot,
        mascot_name: mascotName,
        tier,
        tier_label: tierLabel,
      },
      payment_intent_data: {
        receipt_email: email || undefined,
        metadata: {
          mascot,
          tier,
          product: `${mascotName} — ${tierLabel}`,
        },
      },
      success_url: `${baseUrl}/success.html?session_id={CHECKOUT_SESSION_ID}&mascot=${mascot}&tier=${tier}`,
      cancel_url: `${baseUrl}/?canceled=1#tarifs`,
      locale: 'fr',
      custom_text: {
        submit: {
          message: `Votre pack ${mascotName} sera livré immédiatement après le paiement. Un reçu vous sera envoyé par email. Achat unique — aucun abonnement.`,
        },
      },
      invoice_creation: {
        enabled: true,
        invoice_data: {
          description: `Achat Uko UI : Pack ${mascotName} (${tierLabel}) — Licence perpétuelle`,
          footer: 'Merci pour votre confiance ! Licence commerciale perpétuelle accordée pour vos projets web & mobiles — Uko UI (https://uko-ui.vercel.app)',
          custom_fields: [
            { name: 'Licence', value: 'Commerciale Perpétuelle' },
            { name: 'Mascotte', value: mascotName },
            { name: 'Support', value: 'aada.entreprise@gmail.com' },
          ],
          metadata: { mascot, tier, mascotName, tierLabel },
          rendering_options: { amount_tax_display: 'include_inclusive_tax' },
        },
      },
      tax_id_collection: { enabled: true },
      automatic_tax: { enabled: true },
      allow_promotion_codes: true,
    };

    const session = await stripe.checkout.sessions.create(sessionParams);

    return res.status(200).json({ url: session.url, sessionId: session.id });
  } catch (err) {
    console.error('[Stripe] create-checkout-session error:', err.message);
    return res.status(500).json({ error: err.message });
  }
}
