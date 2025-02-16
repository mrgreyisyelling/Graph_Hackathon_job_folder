<%*
const { moment, app } = tp;
const today = moment().format("YYYY-MM-DD");
const dailyFolder = `Daily/${today}`;

async function updateDailyNote() {
    const uniqueNotes = app.vault.getMarkdownFiles().filter(f => 
        f.path.startsWith(dailyFolder) && f.basename !== today
    );

    if (uniqueNotes.length > 0) {
        let links = uniqueNotes.map(f => `- [[${f.basename}]]`).join("\n");
        let content = await app.vault.read(tp.file);
        let updatedContent = content.replace("## Unique Notes", `## Unique Notes\n${links}`);
        await app.vault.modify(tp.file, updatedContent);
    }
}

updateDailyNote();
%>
