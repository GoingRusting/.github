# Finish the organization settings

The profile README, branding assets, and community templates are repository files. Organization settings, repository About panels, avatar uploads, and public pins are separate GitHub controls.

## Descriptions and topics

[settings.json](settings.json) contains the prepared organization description and all five repository descriptions and topic lists.

With an authenticated GitHub CLI and an organization-owner account, run:

```sh
python3 setup/apply-settings.py          # preview the changes
python3 setup/apply-settings.py --apply  # publish and verify them
```

The script checks access to all repositories before writing. It preserves existing topics and changes only descriptions and topics. Run it from this repository's checkout; it resolves the settings file relative to the script.

Alternatively, update the organization description in [organization settings](https://github.com/organizations/GoingRusting/settings/profile), then use the gear beside **About** on each repository page to enter the prepared description and topics.

## Avatar

Download [avatar.png](../assets/avatar.png), then open [organization profile settings](https://github.com/organizations/GoingRusting/settings/profile). Under the profile picture, choose **Upload new picture** and upload the image. The square copper G matches the banner; its source is [avatar.svg](../assets/avatar.svg).

## Public pinned repositories

Open [GoingRusting](https://github.com/GoingRusting), select **View as: Public**, and choose **Customize pins** or **pin repositories**. Select these three projects:

1. RustingEngine
2. RustingBrain
3. RustingShader

Save the selection. The profile README also features these projects with descriptions and getting-started links.

## Branding

- Background: `#16191d`
- Copper: `#ef925e`
- Cream: `#f5eee3`
- Banner: [PNG](../assets/banner.png) · [SVG source](../assets/banner.svg)
- Avatar: [PNG](../assets/avatar.png) · [SVG source](../assets/avatar.svg)

Keep the same mark and palette for future project artwork. Use actual project screenshots and clear project names, and keep text readable at small sizes.
