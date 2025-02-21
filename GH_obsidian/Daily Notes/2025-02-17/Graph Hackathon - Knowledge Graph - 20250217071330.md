### **📌 Where Should a Listing Be Stored as Its Own Note?**

Since **listings** (jobs, housing, events, etc.) are **entities** that need their own notes, they should have a **dedicated folder** in the vault while still being **linked across multiple locations**.

---

## **🏗️ Storing Listings as Entities**

A listing should have:

1. **Its own note as an entity.**
2. **A dedicated folder for easy access.**
3. **Multiple links in other relevant notes.**

---

### **🏡 File Structure for Listings**

📂 `02-Live`

- 📂 **Listings (`/listings/`)** → **Dedicated home for all listings.**
    - `/listings/jobs/` → **Job listings**
        - `/listings/jobs/2025-02-17-barista-coffee-shop.md`
    - `/listings/housing/` → **Rental/sale listings**
        - `/listings/housing/2025-02-15-apartment-main-st.md`
    - `/listings/events/` → **Community events**
        - `/listings/events/2025-03-01-live-music-concert.md`
    - `/listings/services/` → **Local service providers**
        - `/listings/services/2025-02-12-childcare-mary-smith.md`

📂 `02-Live/topics`

- `/topics/jobs/job_listings.md` → **Links to jobs**
- `/topics/housing/available_rentals.md` → **Links to rentals**
- `/topics/events/upcoming_events.md` → **Links to events**
- `/topics/services/childcare.md` → **Links to services**

📂 `02-Live/community_nodes`

- `/community_nodes/bulletin_boards/Coffee_Shop.md` → **Links local job postings**
- `/community_nodes/neighborhoods/Eastside.md` → **Links jobs in Eastside**
- `/community_nodes/landmarks/Michigan_Avenue.md` → **Links jobs on Michigan Ave**

📂 `02-Live/discussion_threads`

- `/discussion_threads/community_questions.md` → **Q&A about listings**
- `/discussion_threads/moderator_notes.md` → **Edits/flagging**
- `/discussion_threads/reviews.md` → **Reviews of services, landlords, jobs**

📂 `01-Export`

- `/01-Export/triples_export.json` → **Structured data for graph analysis**

---

## **📜 Example Job Listing Note**

📄 `/listings/jobs/2025-02-17-barista-coffee-shop.md`

```yaml
---
entity: "Job Listing"
title: "Part-Time Barista at Coffee Shop"
posted_on: "2025-02-17"
location: "Coffee Shop"
pay: "$15/hr + tips"
hours: "20 hrs/week"
contact: "[[User_007]]"
linked_nodes:
  - "[[Coffee_Shop]]"
  - "[[Eastside]]"
  - "[[job_listings]]"
discussion: "[[community_questions]]"
---
```

**🔗 Links appear in**:

- `job_listings.md` (index of all jobs)
- `Coffee_Shop.md` (bulletin board)
- `Eastside.md` (geographic location)
- `community_questions.md` (if discussed)

---

## **🎯 Why This Works**

✅ **Each listing has its own entity note.**  
✅ **Listings are easy to find inside `/listings/`.**  
✅ **They are linked across relevant locations for discoverability.**  
✅ **The graph structure makes navigation flexible and non-hierarchical.**

---

## **🚀 Next Steps**

4. **Do you want me to generate sample listing notes?**
5. **Would you like a script to auto-create these with randomized data?**
6. **Do you want a way to “expire” listings over time?**