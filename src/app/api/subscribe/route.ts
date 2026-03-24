import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  const { email } = await req.json();

  if (!email || !email.includes("@")) {
    return NextResponse.json({ error: "Valid email required" }, { status: 400 });
  }

  const formId = process.env.KIT_FORM_ID;
  const apiKey = process.env.KIT_API_KEY;

  if (!formId || !apiKey) {
    console.error("Missing KIT_FORM_ID or KIT_API_KEY");
    return NextResponse.json({ error: "Server misconfigured" }, { status: 500 });
  }

  const res = await fetch(
    `https://api.convertkit.com/v3/forms/${formId}/subscribe`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ api_key: apiKey, email }),
    }
  );

  if (!res.ok) {
    const body = await res.text();
    console.error("Kit API error:", res.status, body);
    return NextResponse.json({ error: "Subscription failed" }, { status: 502 });
  }

  return NextResponse.json({ ok: true });
}
