import { useState } from "react";
import { AppProvider } from "@/store/AppStore";
import { Sidebar, MobileTabs, type View } from "@/components/dashboard/Sidebar";
import { UploadView } from "@/views/UploadView";
import { PreviewView } from "@/views/PreviewView";
import { VisualizeView } from "@/views/VisualizeView";
import { InsightsView } from "@/views/InsightsView";
import { ReportView } from "@/views/ReportView";
import { ChatView } from "@/views/ChatView";

function Shell() {
  const [view, setView] = useState<View>("upload");
  const renderView = () => {
    switch (view) {
      case "upload": return <UploadView />;
      case "preview": return <PreviewView />;
      case "visualize": return <VisualizeView />;
      case "insights": return <InsightsView />;
      case "report": return <ReportView />;
      case "chat": return <ChatView />;
    }
  };
  return (
    <div className="flex min-h-screen bg-background text-foreground">
      <Sidebar view={view} onChange={setView} />
      <div className="flex-1 flex flex-col min-w-0">
        <MobileTabs view={view} onChange={setView} />
        <main className="flex-1 p-6 md:p-8 overflow-x-hidden">{renderView()}</main>
      </div>
    </div>
  );
}

const Index = () => (
  <AppProvider>
    <Shell />
  </AppProvider>
);

export default Index;
