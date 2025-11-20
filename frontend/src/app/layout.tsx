import type { Metadata } from "next"
import { Inter } from "next/font/google"
import './globals.css'

const inter = Inter ({subsets: ['latin']})

export const metadata: Metadata = {
    title: "Generador de Configuraciones",
    description: "Generador de Configuraciones para equipos de Red",
}

export default function RootLayout ({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="es">
      <body className={inter.className}>{children}</body>
    </html>
  )
}