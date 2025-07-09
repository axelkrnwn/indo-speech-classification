import { writeFile } from '@tauri-apps/plugin-fs';
import { appDataDir } from '@tauri-apps/api/path';
import { Command } from '@tauri-apps/plugin-shell';

async function sendBlobAsFile(blob: Blob) {
  const buffer = await blob.arrayBuffer();
  const filePath = (await appDataDir()) + "\\temp_audio.wav";

  console.log(filePath)
  
  try {
    let result = await writeFile(filePath, new Uint8Array(buffer))
    console.log(result);
  } catch (e) {
    console.warn('Command failed:', e);
  }
  console.log('done writing file')
  try {
    console.log('hehe')
    const output = await Command.sidecar('binaries/test', [filePath]).execute();
    console.log('stdout', output);
    return output.stdout
  } catch (err) {
    console.error('Sidecar error:', err);
    return ""
  }
}

export {sendBlobAsFile}