import { Component, ElementRef, ViewChild, signal } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; // ✅ ADD THIS
import { ChangeDetectorRef } from '@angular/core';
import { computed } from '@angular/core';


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule], // ✅ ADD HERE
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  Object = Object;
  activeTab = signal<'extracted' | 'chat' | 'api'>('extracted');

  selectedFileName = signal<string | null>(null);
  private _selectedFileUrl: SafeResourceUrl | null = null;

  sessionId = signal<string | null>(null);

  classification = signal<any>(null);
  extractedData = signal<any>(null);

  chatMessages = signal<any[]>([]);
  chatInput = signal<string>('');
  copiedResponse = signal(false);
  copiedRequest = signal(false);
  copiedEndpoint = signal(false);
  isLoading = signal(false);
  isUploading = signal(false);     // upload in progress
  isExtracting = signal(false);    // after sessionId, before extract done
  isDragging = signal(false);
  isThinking = signal(false);
  entries = computed(() => {
  const data = this.extractedData();
  if (!data) return [];
  return Object.entries(data);
});

  @ViewChild('fileInput') fileInput?: ElementRef<HTMLInputElement>;
  @ViewChild('chatContainer') chatContainer?: ElementRef;

  constructor(private sanitizer: DomSanitizer,private cdr: ChangeDetectorRef) {}

  // ---------------- TAB ----------------
  setTab(tab: 'extracted' | 'chat' | 'api') {
    this.activeTab.set(tab);
  }

  // ---------------- FILE UPLOAD ----------------
  onUploadClick() {
    this.fileInput?.nativeElement.click();
  }

  async onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files && input.files[0];

    if (!file) return;

    this.selectedFileName.set(file.name);

    const objectUrl = URL.createObjectURL(file);
    this._selectedFileUrl =
      this.sanitizer.bypassSecurityTrustResourceUrl(objectUrl);

    input.value = '';

    // 🔥 CALL BACKEND UPLOAD API
    this.handleFile(file);
  }

  selectedFileUrl(): SafeResourceUrl | null {
    return this._selectedFileUrl;
  }

  // ---------------- API CALLS ----------------

  async uploadPdf(file: File) {
  this.isLoading.set(true);   // ✅ START LOADER
  this.resetChat();

  const formData = new FormData();
  formData.append('file', file);

  try {
    const res: any = await fetch('http://127.0.0.1:8000/upload-pdf', {
      method: 'POST',
      body: formData
    });

    const data = await res.json();

    this.sessionId.set(data.session_id);
    this.classification.set(data.classification_result);
    this.isUploading.set(false);
    this.isExtracting.set(true);
    this.isLoading.set(false);

    await this.extractData();

  } catch (err) {
    console.error(err);
    this.isLoading.set(false);
  } finally {
    this.isLoading.set(false);  // ✅ STOP LOADER
  }
}
  async extractData() {
    if (!this.sessionId()) return;

    try {
      const res: any = await fetch('http://127.0.0.1:8000/api/v1/extract/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          session_id: this.sessionId()
        })
      });

      const data = await res.json();

      console.log('EXTRACT RESPONSE:', data);

      queueMicrotask(() => {
  this.extractedData.set(data.extracted_data);
});
this.cdr.detectChanges();

    } catch (err) {
      console.error('Extract error:', err);
    }
    finally {
    // 🔥 stop loader → show data
    this.isExtracting.set(false);
  }
  }

  // ---------------- CHAT ----------------

  async sendMessage() {
  setTimeout(() => this.scrollToBottom(), 50);
  if (!this.chatInput() || !this.sessionId()) return;

  const userMsg = this.chatInput();

  this.chatMessages.update(m => [...m, { role: 'user', text: userMsg }]);
  this.chatInput.set('');

  this.isThinking.set(true);   // 🔥 START THINKING

  try {
    const res: any = await fetch('http://127.0.0.1:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: this.sessionId(),
        query: userMsg
      })
    });

    const data = await res.json();

    this.chatMessages.update(m => [
      ...m,
      { role: 'ai', text: data.response }
    ]);

  } catch (err) {
    console.error(err);
  } finally {
    this.isThinking.set(false);  // 🔥 STOP
    setTimeout(() => this.scrollToBottom(), 50);
  }
}
  copyRequest() {
  const text = JSON.stringify({
    session_id: this.sessionId() || 'No Session'
  }, null, 2);

  navigator.clipboard.writeText(text).then(() => {
    this.copiedRequest.set(true);

    setTimeout(() => this.copiedRequest.set(false), 1500);
  });
}

copyResponse() {
  const data = this.extractedData();
  if (!data) return;

  const text = JSON.stringify(data, null, 2);

  navigator.clipboard.writeText(text).then(() => {
    this.copiedResponse.set(true);

    // revert after 1.5 sec
    setTimeout(() => this.copiedResponse.set(false), 1500);
  });
}
copyEndpoint() {
  const text = `http://127.0.0.1:8000/api/v1/extract/`;

  navigator.clipboard.writeText(text).then(() => {
    this.copiedEndpoint.set(true);

    setTimeout(() => this.copiedEndpoint.set(false), 1500);
  });
}
onDragOver(event: DragEvent) {
  event.preventDefault();
  this.isDragging.set(true);
}

onDragLeave(event: DragEvent) {
  event.preventDefault();
  this.isDragging.set(false);
}

onDrop(event: DragEvent) {
  event.preventDefault();
  this.isDragging.set(false);

  const file = event.dataTransfer?.files?.[0];

  if (file) {
    this.handleFile(file);
  }
}
async handleFile(file: File) {
  this.selectedFileName.set(file.name);

  const objectUrl = URL.createObjectURL(file);
  this._selectedFileUrl =
    this.sanitizer.bypassSecurityTrustResourceUrl(objectUrl);

  await this.uploadPdf(file);
}
scrollToBottom() {
  try {
    const el = this.chatContainer?.nativeElement;
    el.scrollTop = el.scrollHeight;
  } catch {}
}
resetChat() {
  this.chatMessages.set([]);
  this.chatInput.set('');
  this.isThinking.set(false);

  // optional: scroll reset
  setTimeout(() => this.scrollToBottom(), 50);
}
}