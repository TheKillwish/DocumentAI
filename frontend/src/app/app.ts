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
  entries = computed(() => {
  const data = this.extractedData();
  if (!data) return [];
  return Object.entries(data);
});

  @ViewChild('fileInput') fileInput?: ElementRef<HTMLInputElement>;

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
    await this.uploadPdf(file);
  }

  selectedFileUrl(): SafeResourceUrl | null {
    return this._selectedFileUrl;
  }

  // ---------------- API CALLS ----------------

  async uploadPdf(file: File) {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res: any = await fetch('http://127.0.0.1:8000/upload-pdf', {
        method: 'POST',
        body: formData
      });

      const data = await res.json();

      console.log('UPLOAD RESPONSE:', data);

      // ✅ Save session
      this.sessionId.set(data.session_id);

      // ✅ Save classification
      this.classification.set(data.classification_result);

      // 🔥 AUTO CALL EXTRACT
      await new Promise(res => setTimeout(res, 1000));
      await this.extractData();

    } catch (err) {
      console.error('Upload error:', err);
    }
  }
  async extractData() {
    if (!this.sessionId()) return;

    try {
      const res: any = await fetch('http://127.0.0.1:8000/extract-data', {
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
  }

  // ---------------- CHAT ----------------

  async sendMessage() {
    if (!this.chatInput() || !this.sessionId()) return;

    const userMsg = this.chatInput();

    // add user message
    this.chatMessages.update(m => [...m, { role: 'user', text: userMsg }]);

    this.chatInput.set('');

    try {
      const res: any = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          session_id: this.sessionId(),
          query: userMsg
        })
      });

      const data = await res.json();

      // add AI response
      this.chatMessages.update(m => [
        ...m,
        { role: 'ai', text: data.response }
      ]);

    } catch (err) {
      console.error('Chat error:', err);
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
  const text = `/api/v1/extract/${this.sessionId() || 'No Session'}`;

  navigator.clipboard.writeText(text).then(() => {
    this.copiedEndpoint.set(true);

    setTimeout(() => this.copiedEndpoint.set(false), 1500);
  });
}
}