import { useQuery } from "@tanstack/react-query";
import { ScrollArea } from "@workspace/ui/components/scroll-area";
import { apiFetch } from "@/shared/api/fetcher";
import { SCRIPT_SCENES } from "@/shared/lib/constants";
import { ScriptCard } from "./script-card";
import type { ScriptTemplate } from "./script-card";

async function fetchScriptTemplates(): Promise<ScriptTemplate[]> {
  const res = await apiFetch("/api/v1/script-templates");
  if (!res.ok) throw new Error("Failed to fetch script templates");
  return res.json();
}

export function ScriptTemplatePanel() {
  const { data: templates = [] } = useQuery({
    queryKey: ["script-templates"],
    queryFn: fetchScriptTemplates,
    staleTime: 5 * 60 * 1000,
  });

  const grouped = SCRIPT_SCENES.map((scene) => ({
    ...scene,
    templates: templates.filter((t) => t.scene === scene.value),
  }));

  return (
    <div className="flex h-full flex-col border-l">
      <div className="border-b px-4 py-3">
        <h2 className="text-sm font-semibold">话术模板</h2>
      </div>
      <ScrollArea className="flex-1 px-4 py-3">
        <div className="space-y-6">
          {grouped.map((group) => (
            <div key={group.value}>
              <h3 className="mb-2 text-xs font-medium text-muted-foreground uppercase tracking-wider">
                {group.label}
              </h3>
              {group.templates.length > 0 ? (
                <div className="space-y-2">
                  {group.templates.map((t) => (
                    <ScriptCard key={t.id} template={t} />
                  ))}
                </div>
              ) : (
                <p className="text-xs text-muted-foreground/60 italic">
                  暂无模板
                </p>
              )}
            </div>
          ))}
        </div>
      </ScrollArea>
    </div>
  );
}
