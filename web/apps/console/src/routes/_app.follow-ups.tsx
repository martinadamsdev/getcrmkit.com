import { Outlet, createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/_app/follow-ups")({
  component: FollowUpsLayout,
});

function FollowUpsLayout() {
  return <Outlet />;
}
