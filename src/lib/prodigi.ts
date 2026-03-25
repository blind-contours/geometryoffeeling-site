const PRODIGI_SANDBOX_URL = "https://api.sandbox.prodigi.com/v4.0";
const PRODIGI_LIVE_URL = "https://api.prodigi.com/v4.0";

function getBaseUrl() {
  return process.env.PRODIGI_SANDBOX === "true"
    ? PRODIGI_SANDBOX_URL
    : PRODIGI_LIVE_URL;
}

function getApiKey() {
  const key = process.env.PRODIGI_API_KEY;
  if (!key) throw new Error("PRODIGI_API_KEY is not set");
  return key;
}

interface Recipient {
  name: string;
  address: {
    line1: string;
    line2?: string;
    postalOrZipCode: string;
    countryCode: string;
    townOrCity: string;
    stateOrCounty?: string;
  };
}

export async function createOrder(
  recipient: Recipient,
  sku: string,
  imageUrl: string,
  merchantReference: string,
  idempotencyKey: string
) {
  const res = await fetch(`${getBaseUrl()}/Orders`, {
    method: "POST",
    headers: {
      "X-API-Key": getApiKey(),
      "Content-Type": "application/json",
      "Idempotency-Key": idempotencyKey,
    },
    body: JSON.stringify({
      merchantReference,
      shippingMethod: "Standard",
      recipient,
      items: [
        {
          merchantReference,
          sku,
          copies: 1,
          sizing: "fitPrintArea",
          assets: [
            {
              printArea: "default",
              url: imageUrl,
            },
          ],
        },
      ],
    }),
  });

  if (!res.ok) {
    const body = await res.text();
    throw new Error(`Prodigi order failed (${res.status}): ${body}`);
  }

  return res.json();
}
