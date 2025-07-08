import { writeFile } from '@tauri-apps/plugin-fs';
import { appDataDir } from '@tauri-apps/api/path';
import { Command } from '@tauri-apps/plugin-shell';

async function sendBlobAsFile(blob: Blob) {
  const buffer = await blob.arrayBuffer();
  const filePath = (await appDataDir()) + "/temp_audio.wav";

  console.log(filePath)

  await writeFile(filePath, new Uint8Array(buffer))

  const command = Command.sidecar('test', [filePath]);
  command.stdout.on('data', console.log);
  command.stderr.on('data', console.error);
  
  const output = await command.execute();
  console.log(output)
  return output
}

export {sendBlobAsFile}