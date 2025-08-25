import os
import re
import yaml

def extract_title_from_filename(filename):
    # Dosya ad\u0131ndan ba\u015fl\u0131k \u00e7\u0131kar.
    title = os.path.splitext(filename)[0]  # Uzant\u0131y\u0131 kald\u0131r
    title = title.replace('-', ' ').replace('_', ' ')  # Tire ve alt \u00e7izgileri bo\u015flukla de\u011fi\u015ftir
    return title.title()  # Ba\u015f harfleri b\u00fcy\u00fck yap


def generate_metadata(file_path, content):
    # Metadata olu\u015ftur.
    filename = os.path.basename(file_path)
    title = extract_title_from_filename(filename)
    
    # A\u00e7\u0131klamay\u0131 olu\u015ftur (basit bir varsay\u0131lan)
    description = f"Information about {title.lower()} on Momtur website."
    
    # Anahtar kelimeleri olu\u015ftur (basit bir varsay\u0131lan)
    keywords = f"{title.lower()}, momtur, bodrum, transfer"
    
    # OG g\u00f6rseli (varsay\u0131lan)
    og_image = "https://res.cloudinary.com/djzzikcey/image/upload/v1753431200/momtur_luxury_transfer_bodrum_hero.jpg"
    
    metadata = {
        'title': title,
        'description': description,
        'keywords': keywords,
        'og': {
            'image': og_image
        }
    }
    
    return metadata

def process_file(file_path):
    # Tek bir dosyay\u0131 i\u015fle.
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Metadata kontrol\u00fc
    has_metadata = content.strip().startswith('---')
    if not has_metadata:
        print(f"  -> Metadata eklenecek: {file_path}")
        metadata = generate_metadata(file_path, content)
        metadata_str = yaml.dump(metadata, default_flow_style=False, allow_unicode=True)
        new_content = f"---\n{metadata_str}---\n\n"
        
        # H1 etiketi kontrol\u00fc ve d\u00fczeltme
        h1_matches = list(re.finditer(r'^#\s+(.*)', content, re.MULTILINE))
        if not h1_matches:
            # H1 etiketi yok, dosya ad\u0131ndan olu\u015ftur
            title_from_filename = extract_title_from_filename(os.path.basename(file_path))
            new_content += f"# {title_from_filename}\n\n"
            print(f"  -> H1 etiketi eklendi (dosya ad\u0131ndan): {title_from_filename}")
        elif len(h1_matches) > 1:
            # Birden fazla H1 etiketi var, ilkini b\u0131rak, di\u011ferlerini H2 yap
            print(f"  -> Birden fazla H1 etiketi bulundu, d\u00fczeltiliyor...")
            # \u0130lk H1'yi koru
            first_h1 = h1_matches[0]
            new_content += content[:first_h1.start()]
            new_content += first_h1.group(0)  # \u0130lk H1'yi oldu\u011fu gibi ekle
            remaining_content = content[first_h1.end():]
            
            # Kalan i\u00e7erikteki di\u011fer H1'leri H2'ye \u00e7evir
            remaining_content = re.sub(r'^#\s+(.*)', r'## \1', remaining_content, flags=re.MULTILINE)
            new_content += remaining_content
        else:
            # Tek H1 etiketi var, i\u00e7eri\u011fi oldu\u011fu gibi ekle
            new_content += content
            
        # Dosyay\u0131 g\u00fcncelle
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
    else:
        print(f"  -> Zaten metadata var: {file_path}")
        # Metadata zaten var, H1 etiketlerini kontrol et
        # Metadata blo\u011funu ay\u0131r
        metadata_end = content.find('---', 3)  # \u0130lk ---'dan sonraki ikinci ---
        if metadata_end != -1:
            # metadata_block = content[4:metadata_end]  # --- ... --- aras\u0131ndaki k\u0131s\u0131m
            remaining_content = content[metadata_end + 3:].lstrip() # Metadata'dan sonraki i\u00e7erik
            
            # H1 etiketi kontrol\u00fc ve d\u00fczeltme
            h1_matches = list(re.finditer(r'^#\s+(.*)', remaining_content, re.MULTILINE))
            if not h1_matches:
                # H1 etiketi yok, dosya ad\u0131ndan olu\u015ftur
                title_from_filename = extract_title_from_filename(os.path.basename(file_path))
                new_remaining_content = f"# {title_from_filename}\n\n" + remaining_content
                print(f"  -> H1 etiketi eklendi (dosya ad\u0131ndan): {title_from_filename}")
                
                # Dosyay\u0131 g\u00fcncelle
                new_content = content[:metadata_end + 3] + '\n\n' + new_remaining_content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                    
            elif len(h1_matches) > 1:
                # Birden fazla H1 etiketi var, ilkini b\u0131rak, di\u011ferlerini H2 yap
                print(f"  -> Birden fazla H1 etiketi bulundu, d\u00fczeltiliyor...")
                # \u0130lk H1'yi koru
                first_h1 = h1_matches[0]
                new_remaining_content = remaining_content[:first_h1.start()]
                new_remaining_content += first_h1.group(0)  # \u0130lk H1'yi oldu\u011fu gibi ekle
                remaining_after_first = remaining_content[first_h1.end():]
                
                # Kalan i\u00e7erikteki di\u011fer H1'leri H2'ye \u00e7evir
                new_remaining_content += re.sub(r'^#\s+(.*)', r'## \1', remaining_after_first, flags=re.MULTILINE)
                
                # Dosyay\u0131 g\u00fcncelle
                new_content = content[:metadata_end + 3] + '\n\n' + new_remaining_content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            else:
                # Tek H1 etiketi var, kontrol et
                h1_title = h1_matches[0].group(1).strip()
                if len(h1_title) < 5 or h1_title.lower() in ['home', 'index']:
                    # H1 \u00e7ok k\u0131sa veya genel, d\u00fczenle
                    title_from_filename = extract_title_from_filename(os.path.basename(file_path))
                    print(f"  -> H1 etiketi \u00e7ok k\u0131sa/genel, d\u00fczeltiliyor: '{h1_title}' -> '{title_from_filename}'")
                    new_remaining_content = re.sub(r'^#\s+.*', f'# {title_from_filename}', remaining_content, count=1, flags=re.MULTILINE)
                    
                    # Dosyay\u0131 g\u00fcncelle
                    new_content = content[:metadata_end + 3] + '\n\n' + new_remaining_content
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                        
    print(f"  -> \u0130\u015flendi: {file_path}")

def main():
    # Ana fonksiyon.
    base_path = '/home/momtur/momtur-docs-1'
    md_files = []
    for root, dirs, files in os.walk(base_path):
        # .git ve node_modules dizinlerini atla
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '.claude']]
        for file in files:
            if file.endswith(('.mdx', '.md')):
                md_files.append(os.path.join(root, file))
    
    print(f"Toplam {len(md_files)} dosya bulundu. \u0130\u015fleniyor...")
    
    for file_path in md_files:
        try:
            process_file(file_path)
        except Exception as e:
            print(f"  -> HATA: {file_path} i\u015flenirken hata olu\u015ftu: {e}")

if __name__ == '__main__':
    main()