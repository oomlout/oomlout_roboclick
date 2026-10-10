step_id: step_01
step_name: Research Source
description: Extracts structured indexes from source transcripts and produces the producer brief.
files:
  - name: story_guide.md
    destination: production/03_story/story_guide.md
    description: Producer narrative brief for the show
  - name: source_synthesis.md
    destination: production/00_admin/source_synthesis.md
    description: Cross-chat narrative synthesis
  - name: characters.json
    destination: source/processed/structured/characters.json
    description: Character index extracted from source
  - name: places.json
    destination: source/processed/structured/places.json
    description: Place index extracted from source
  - name: song_seeds.json
    destination: source/processed/structured/song_seeds.json
    description: Song seed ideas extracted from source
  - name: lyric_fragments.json
    destination: source/processed/structured/lyric_fragments.json
    description: Lyric fragments extracted from source
  - name: themes.json
    destination: source/processed/structured/themes.json
    description: Themes extracted from source
  - name: narrative_threads.json
    destination: source/processed/structured/narrative_threads.json
    description: Narrative threads extracted from source
  - name: facts.json
    destination: source/processed/structured/facts.json
    description: Facts extracted from source
  - name: craft_notes.json
    destination: source/processed/structured/craft_notes.json
    description: Craft notes extracted from source
  - name: open_questions.json
    destination: source/processed/structured/open_questions.json
    description: Open questions extracted from source
  - name: conflicts.json
    destination: source/processed/structured/conflicts.json
    description: Conflicts extracted from source
