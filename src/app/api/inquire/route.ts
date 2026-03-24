import { NextRequest, NextResponse } from "next/server";
import { Resend } from "resend";

const FROM = "Geometry of Feeling <onboarding@resend.dev>";

function getResend() {
  const key = process.env.RESEND_API_KEY;
  if (!key) throw new Error("RESEND_API_KEY is not set");
  return new Resend(key);
}

export async function POST(req: NextRequest) {
  const { name, email, piece, description } = await req.json();

  if (!name || !email || !email.includes("@") || !description) {
    return NextResponse.json(
      { error: "Name, email, and description are required" },
      { status: 400 }
    );
  }

  const artistEmail = process.env.ARTIST_EMAIL || "hello@geometryoffeeling.com";

  try {
    const { error } = await getResend().emails.send({
      from: FROM,
      to: artistEmail,
      replyTo: email,
      subject: `Custom print inquiry from ${name}`,
      html: `
<div style="font-family:'Courier New',monospace;max-width:560px;margin:0 auto;padding:24px;">
  <p style="font-size:12px;letter-spacing:0.15em;text-transform:uppercase;color:#888;margin-bottom:24px;">
    Custom Print Inquiry
  </p>
  <p><strong>Name:</strong> ${name}</p>
  <p><strong>Email:</strong> ${email}</p>
  ${piece ? `<p><strong>Piece/Series:</strong> ${piece}</p>` : ""}
  <hr style="border:none;border-top:1px solid #E0DDD8;margin:16px 0;" />
  <p style="white-space:pre-wrap;">${description}</p>
</div>
      `.trim(),
    });

    if (error) {
      console.error("Failed to send inquiry email:", error);
      return NextResponse.json({ error: "Email failed" }, { status: 502 });
    }

    return NextResponse.json({ ok: true });
  } catch (err) {
    console.error("Inquiry route error:", err);
    return NextResponse.json({ error: "Server error" }, { status: 500 });
  }
}
