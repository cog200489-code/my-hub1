// 사용법: node transcribe.mjs input.mp4 output.srt
// 영상에서 음성을 뽑아 Whisper(small)로 한국어 자막(SRT)을 만듭니다.
import { pipeline, env } from '@huggingface/transformers';
import { execFileSync } from 'node:child_process';
import { writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
env.localModelPath = path.join(here, 'node_modules/sts-whisper-small/models/');
env.allowRemoteModels = false;

const [input, output] = process.argv.slice(2);
// 16kHz 모노 32bit float 원시 오디오로 변환
const raw = execFileSync('ffmpeg', ['-v', 'error', '-i', input, '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], { maxBuffer: 1 << 30 });
const audio = new Float32Array(raw.buffer, raw.byteOffset, raw.length / 4);

const asr = await pipeline('automatic-speech-recognition', 'Xenova/whisper-small', { dtype: 'q8' });
const res = await asr(audio, { language: 'korean', task: 'transcribe', return_timestamps: true, chunk_length_s: 30, stride_length_s: 5 });

const ts = (s) => {
  const ms = Math.round(s * 1000);
  const p = (n, w = 2) => String(n).padStart(w, '0');
  return `${p(Math.floor(ms / 3600000))}:${p(Math.floor(ms / 60000) % 60)}:${p(Math.floor(ms / 1000) % 60)},${p(ms % 1000, 3)}`;
};
const dur = audio.length / 16000;
const srt = res.chunks.map((c, i) => {
  const [a, b] = c.timestamp;
  return `${i + 1}\n${ts(a)} --> ${ts(b ?? dur)}\n${c.text.trim()}\n`;
}).join('\n');
writeFileSync(output, srt);
console.log(srt);
