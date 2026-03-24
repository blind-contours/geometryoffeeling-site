import { Resend } from "resend";

const resend = new Resend(process.env.RESEND_API_KEY);

// Until you verify your domain in Resend, use their test sender.
// After verification, change to: "Geometry of Feeling <hello@geometryoffeeling.com>"
const FROM = "Geometry of Feeling <onboarding@resend.dev>";

interface OrderEmailParams {
  to: string;
  customerName: string;
  pieceTitle: string;
  sizeLabel: string;
  imageUrl: string;
  equation: string;
}

export async function sendOrderConfirmation({
  to,
  customerName,
  pieceTitle,
  sizeLabel,
  imageUrl,
  equation,
}: OrderEmailParams) {
  const { error } = await resend.emails.send({
    from: FROM,
    to,
    subject: `Your print is on its way — ${pieceTitle}`,
    html: `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body style="margin:0;padding:0;background:#FAFAF8;font-family:'Courier New',monospace;color:#1A1A18;">
  <div style="max-width:560px;margin:0 auto;padding:40px 24px;">

    <p style="font-size:12px;letter-spacing:0.15em;text-transform:uppercase;color:#888;margin-bottom:32px;">
      Geometry of Feeling
    </p>

    <h1 style="font-size:22px;font-weight:300;margin-bottom:8px;">
      Thank you${customerName ? `, ${customerName}` : ""}.
    </h1>

    <p style="font-size:15px;color:#555;line-height:1.6;margin-bottom:32px;">
      Your print of <strong>${pieceTitle}</strong> (${sizeLabel}) is being prepared
      on Hahnem&uuml;hle German Etching 310gsm paper. You'll receive a tracking
      email once it ships — typically 5–10 business days.
    </p>

    <div style="background:#F0EDE8;padding:4px;margin-bottom:24px;">
      <img src="${imageUrl}" alt="${pieceTitle}" style="width:100%;display:block;" />
    </div>

    <p style="font-size:13px;color:#888;font-style:italic;margin-bottom:32px;">
      ${equation}
    </p>

    <hr style="border:none;border-top:1px solid #E0DDD8;margin:32px 0;" />

    <p style="font-size:13px;color:#888;line-height:1.6;">
      Every piece begins with a human emotion and asks: what mathematical function
      has the same shape as this feeling? The equation isn't decoration — it's the
      reason the piece looks the way it does.
    </p>

    <p style="font-size:12px;color:#AAA;margin-top:32px;">
      geometryoffeeling.com
    </p>

  </div>
</body>
</html>
    `.trim(),
  });

  if (error) {
    console.error("Failed to send order confirmation:", error);
    throw error;
  }
}
