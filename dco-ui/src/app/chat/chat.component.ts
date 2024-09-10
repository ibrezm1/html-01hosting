import { Component, ElementRef, ViewChild, AfterViewChecked } from '@angular/core';
import { StreamService } from '../stream.service';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent {
  @ViewChild('chatMessagesRef') private chatMessagesContainer!: ElementRef;

  message: string = '';
  model: string = 'default'; // Assuming 'model' is chosen by user somewhere
  showProcessing: boolean = false;

  constructor(private streamService: StreamService) {}

  chatMessages: { user: string; message: string; type: string }[] = [
    { user: 'User', message: 'How can I find the right dataset for customer analytics?', type: 'user' },
    {
      user: 'AI',
      message: 'To find the right dataset for customer analytics, you can use the data catalog’s search feature. Look for keywords like "customer transactions," "purchase history," or "customer demographics." You can also filter by the business domain or data asset type.',
      type: 'ai'
    },
    { user: 'User', message: 'Can I view metadata for each dataset before downloading?', type: 'user' },
    {
      user: 'AI',
      message: 'Yes, the data catalog provides metadata such as the dataset description, creation date, data owner, and schema. This will help you assess if the dataset is relevant for your needs before downloading it.',
      type: 'ai'
    },
    { user: 'User', message: 'What are the key attributes to look for in a high-quality dataset?', type: 'user' },
    {
      user: 'AI',
      message: 'Key attributes include data accuracy, completeness, consistency, and relevance to your analysis goals. It’s also important to check the dataset’s update frequency and whether it includes proper documentation.',
      type: 'ai'
    },
    { user: 'User', message: 'How do I filter datasets by specific business domains?', type: 'user' },
    {
      user: 'AI',
      message: 'You can filter datasets by business domains using the sidebar or advanced search options. Select domains like "Marketing," "Sales," or "Finance" to narrow down your dataset search.',
      type: 'ai'
    },
    { user: 'User', message: 'How often is the data catalog updated with new datasets?', type: 'user' },
    {
      user: 'AI',
      message: 'The data catalog is regularly updated by data stewards and administrators. You can check the "Last Updated" field in the metadata section of each dataset to see when it was last refreshed or modified.',
      type: 'ai'
    },
    { user: 'User', message: 'Can I contribute to the data catalog?', type: 'user' },
    {
      user: 'AI',
      message: 'Yes, if you have the necessary permissions, you can contribute to the data catalog by uploading new datasets or updating existing ones. Make sure to provide complete metadata and follow the catalog’s data quality standards.',
      type: 'ai'
    },
    { user: 'User', message: 'How can I assess the data quality of a dataset?', type: 'user' },
    {
      user: 'AI',
      message: 'You can assess the data quality by reviewing the data quality reports provided in the metadata section. Look for metrics like completeness, accuracy, and timeliness to ensure the dataset meets your requirements.',
      type: 'ai'
    },
  ];

  ngAfterViewChecked() {
    this.scrollToBottom();
  }

  scrollToBottom(): void {
    try {
      this.chatMessagesContainer.nativeElement.scrollTop = this.chatMessagesContainer.nativeElement.scrollHeight;
    } catch (err) {
      console.error('Failed to scroll to bottom', err);
    }
  }

  sendMessage(): void {
    if (!this.message || !this.model) return;  // Ensure there's a message and model before sending
  
    const input = this.message;
    const model = this.model;
  
    // Add the user input to the chat messages array
    this.chatMessages.push({ user: 'User', message: input, type: 'user' });
  
    // Clear the input field after sending
    this.message = '';
  
    // Add an empty AI response message for streaming updates
    this.chatMessages.push({ user: 'AI', message: '', type: 'ai' });
  
    // Show a loading indicator or processing state
    this.showProcessing = true;
  
    // Call the stream service and subscribe to the response stream
    this.streamService.streamMessage(input, model).subscribe(
      (data: string) => {
        // Update the last message with streaming data
        const lastMessageIndex = this.chatMessages.length - 1;
        this.chatMessages[lastMessageIndex] = { ...this.chatMessages[lastMessageIndex], message: data };
  
        // Scroll to the bottom of the chat
        this.scrollToBottom();
      },
      (error: any) => {
        console.error('Error during streaming:', error);
        this.showProcessing = false;
      },
      () => {
        // End of the streaming, disable the loading indicator
        this.showProcessing = false;
        console.log('Streaming complete');
      }
    );
  
    // Scroll to the bottom of the chat after sending the message
    this.scrollToBottom();
  }
}