import { PageHeader } from "@/components/dashboard/PageHeader";
import { ChatWindow } from "@/components/dashboard/ChatWindow";

export function ChatView() {
  return (
    <div>
      <PageHeader title="Chat with your data" subtitle="Ask the LangChain agent questions in natural language." />
      <ChatWindow />
    </div>
  );
}