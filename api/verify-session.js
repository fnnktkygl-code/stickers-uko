// api/verify-session.js
// Vercel Serverless Function — Uko UI Stripe Session Verification

const DOWNLOAD_URLS = {
  aituko: {
    starter: '/downloads/AItuko-Starter-Pack.zip',
    pro:     '/downloads/AItuko-Pro-12-States.zip',
  },
  owluko: {
    starter: '/downloads/Owluko-Starter-Pack.zip',
    pro:     '/downloads/Owluko-Pro-12-States.zip',
  },
  luneko: {
    starter: '/downloads/Luneko-Starter-Pack.zip',
    pro:     '/downloads/Luneko-Pro-12-States.zip',
  },
  hatoko: {
    starter: '/downloads/Hatoko-Starter-Pack.zip',
    pro:     '/downloads/Hatoko-Pro-12-States.zip',
  },
  usako: {
    starter: '/downloads/Usako-Starter-Pack.zip',
    pro:     '/downloads/Usako-Pro-12-States.zip',
  },
};

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });

  const { session_id } = req.query;

  if (!session_id || !session_id.startsWith('cs_')) {
    return res.status(400).json({ error: 'Invalid session ID.' });
  }

  try {
    const stripe = (await import('stripe')).default(process.env.STRIPE_SECRET_KEY);

    const session = await stripe.checkout.sessions.retrieve(session_id);

    if (session.payment_status !== 'paid') {
      return res.status(402).json({ error: 'Payment not completed.', status: session.payment_status });
    }

    const mascot = session.metadata?.mascot || 'aituko';
    const tier   = session.metadata?.tier   || 'starter';

    const downloadUrl = DOWNLOAD_URLS[mascot]?.[tier];

    if (!downloadUrl) {
      return res.status(404).json({ error: 'Download not found for this mascot/tier combination.' });
    }

    let invoiceUrl = null;
    let invoicePdf = null;

    if (session.invoice) {
      try {
        const invoice = await stripe.invoices.retrieve(session.invoice);
        invoiceUrl = invoice.hosted_invoice_url || null;
        invoicePdf = invoice.invoice_pdf || null;
        // Dispatch email automatically
        if (invoice.status === 'paid' && !invoice.sent_at) {
          await stripe.invoices.sendInvoice(session.invoice).catch(() => {});
        }
      } catch (invErr) {
        console.warn('[Stripe] invoice retrieval/send warning:', invErr.message);
      }
    }

    return res.status(200).json({
      success: true,
      mascot,
      tier,
      mascotName:  session.metadata?.mascot_name  || mascot,
      tierLabel:   session.metadata?.tier_label   || tier,
      customerEmail: session.customer_details?.email || null,
      downloadUrl,
      invoiceUrl,
      invoicePdf,
      amountPaid: session.amount_total,
      currency:   session.currency,
    });
  } catch (err) {
    console.error('[Stripe] verify-session error:', err.message);
    return res.status(500).json({ error: err.message });
  }
}
