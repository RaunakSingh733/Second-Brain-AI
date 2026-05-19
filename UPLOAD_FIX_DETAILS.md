"""
API router for Second Brain AI backend - Phase 2 Enhanced.
Includes hybrid search, RAG with citations, and memory-aware chat.
[... continuing from earlier in file ...]
"""

# ============================================================================
# FILE UPLOAD ENDPOINT - FIXED
# ============================================================================

@router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a document, process text, and store embeddings."""
    try:
        from services.file_service import validate_file, save_upload_file
        if not validate_file(file):
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # FIXED: Added 'await' here - was causing 'coroutine' error
        saved_path = await save_upload_file(file)
        ext = saved_path.suffix.lower()
        
        text = ""
        if ext == ".txt":
            from parsers.text_parser import extract_text_from_txt
            text = extract_text_from_txt(saved_path)
        elif ext == ".md":
            from parsers.text_parser import extract_text_from_md
            text = extract_text_from_md(saved_path)
        elif ext == ".pdf":
            from parsers.text_parser import extract_text_from_pdf
            text = extract_text_from_pdf(saved_path)
        elif ext == ".docx":
            from parsers.text_parser import extract_text_from_docx
            text = extract_text_from_docx(saved_path)
        else:
            text = saved_path.read_text(encoding="utf-8", errors="replace")
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text content extracted")
        
        from parsers.text_parser import clean_text, chunk_text
        cleaned = clean_text(text)
        chunks = chunk_text(cleaned, chunk_size=500, overlap=50)
        
        if not chunks:
            raise HTTPException(status_code=400, detail="Text too short")
        
        embeddings = embedding_service.encode_text(chunks)
        import uuid
        chunk_ids = [str(uuid.uuid4()) for _ in chunks]
        file_id = int(time.time() * 1000)
        
        metadatas = [{
            "file_id": file_id,
            "file_name": file.filename,
            "chunk_index": i,
        } for i, chunk in enumerate(chunks)]
        
        vector_store.add_documents(
            ids=chunk_ids, texts=chunks, embeddings=embeddings, metadatas=metadatas
        )
        
        db_service.add_file_record(
            file_id=file_id, filename=file.filename, file_size=os.path.getsize(saved_path)
        )
        
        for i, (chunk, chunk_id) in enumerate(zip(chunks, chunk_ids)):
            db_service.execute_update(
                "INSERT INTO document_chunks (id, file_id, chunk_index, text, source) VALUES (?, ?, ?, ?, ?)",
                (chunk_id, file_id, i, chunk, file.filename),
            )
        
        # Generate summary
        try:
            summary = summary_service.generate_summary(cleaned)
            topics = summary_service.extract_topics(cleaned)
            db_service.update_file_summaries(file_id, summary, "", topics)
        except Exception as se:
            logger.warning("Summary generation failed: " + str(se))
        
        # Rebuild BM25 index
        try:
            retriever.build_bm25_index()
        except Exception as be:
            logger.warning("BM25 rebuild failed: " + str(be))
        
        return {
            "message": "File uploaded and processed successfully",
            "file_id": file_id,
            "filename": file.filename,
            "chunks": len(chunks),
            "file_size": os.path.getsize(saved_path),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
