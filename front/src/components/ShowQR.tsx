import dynamic from 'next/dynamic';

// Динамически импортируем QRCodeSVG без SSR
const QRCodeSVG = dynamic(() => import('qrcode.react').then((mod) => mod.QRCodeSVG), { ssr: false });

export default function ShowQR({ otpauth_url }: { otpauth_url: string }) {
  return (
    <div>
      <h2>Scan this QR code with your 2FA app:</h2>
      {otpauth_url && <QRCodeSVG value={otpauth_url} />}
    </div>
  );
}
