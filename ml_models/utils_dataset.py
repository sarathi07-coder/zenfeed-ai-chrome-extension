import pandas as pd

def create_sample_dataset(save_path="data/processed/sample_dataset.csv"):
    rows = [
    # addictive
    {"title":"Try Not To Laugh - Funny Memes Compilation", "description":"memes and funny videos", "label":"addictive"},
    {"title":"Top 10 Gaming Fails", "description":"gaming compilation", "label":"addictive"},
    {"title":"Endless TikTok memes", "description":"funny, addictive short videos", "label":"addictive"},
    {"title":"Ultimate meme battle", "description":"non-stop memes", "label":"addictive"},

    # educational
    {"title":"Java Tutorial for Beginners - 10 minutes", "description":"learn java basics", "label":"educational"},
    {"title":"What is Machine Learning?", "description":"simple explanation for beginners", "label":"educational"},
    {"title":"Python If Else Tutorial", "description":"learn python basics", "label":"educational"},

    # productive
    {"title":"Study With Me - Pomodoro", "description":"study together", "label":"productive"},
    {"title":"Guided Meditation 10 minutes", "description":"relaxation", "label":"productive"},
    {"title":"Morning routine for focus", "description":"improve productivity", "label":"productive"},

    # neutral
    {"title":"Unboxing new phone", "description":"review", "label":"neutral"},
    {"title":"Top 5 tech gadgets", "description":"neutral tech info", "label":"neutral"},
    {"title":"Room tour setup video", "description":"overview of workspace", "label":"neutral"},
]

    df = pd.DataFrame(rows)
    df.to_csv(save_path, index=False)
    return df

if __name__ == "__main__":
    print("Creating dataset...")
    create_sample_dataset()
    print("Dataset saved!")
