import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ChatDialogComponent } from './components/chat-dialog/chat-dialog.component';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, ChatDialogComponent, FormsModule, HttpClientModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = "LLMEvaluation";
  GPT35 = "GPT 3.5 Turbo";
  GPT4 = "GPT 4"
  llama = "Llama (Not Implemented Yet)"
  falcon = "Falcon (Not Implemented Yet)"
}
