import { NextRequest, NextResponse } from "next/server";
import {harmonizer } from '@/lib/harmonizer'


export async function POST(req: NextRequest) {
    try {
        const formData = await req.formData();
        const file = formData.get('file') as File;
        const style = formData.get('style') as string;
        const complexity = formData.get('complexity') as string;

        const melody = await file.arrayBuffer();
        
        if (!file || !style || !complexity) {
            return NextResponse.json({ error: 'Missing required fields' }, { status: 400 });
        }

        const buffer = Buffer.from(melody);
        const harmonizedBuffer = await harmonizer.harmonize(buffer, style, complexity);


        return new NextResponse(harmonizedBuffer, {
            headers: {
                'Content-Type': 'audio/midi',
                'Content-Disposition': 'attachment; filename="harmonized.mid"'
            }
        });
    } catch (error) {
        console.error('Error harmonizing melody:', error);
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
    }
}


