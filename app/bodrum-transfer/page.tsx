"use client";

import Link from "next/link";
import { Card, CardContent } from "@radix-ui/react-card";
import { FaMapMarkerAlt } from "react-icons/fa";

const mahalleler = [
  { ad: "Bitez", link: "/bodrum-transfer/bitez" },
  { ad: "Gümbet", link: "/bodrum-transfer/gumbet" },
  { ad: "Turgutreis", link: "/bodrum-transfer/turgutreis" },
  { ad: "Yalıkavak", link: "/bodrum-transfer/yalikavak" },
  { ad: "Göltürkbükü", link: "/bodrum-transfer/golturkbuku" }
];

export default function BodrumTransfer() {
  return (
    <main className="min-h-screen px-4 py-8 bg-gray-50">
      <h1 className="text-3xl font-bold mb-8 text-center">Bodrum Transfer</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
        {mahalleler.map((mahalle) => (
          <Link href={mahalle.link} key={mahalle.ad}>
            <Card className="transition-transform duration-200 hover:scale-105 cursor-pointer shadow-md bg-white rounded-lg">
              <CardContent className="flex flex-col items-center p-6">
                <FaMapMarkerAlt className="text-primary text-3xl mb-2" />
                <span className="text-lg font-semibold">{mahalle.ad}</span>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </main>
  );
}
